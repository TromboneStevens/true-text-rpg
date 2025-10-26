#!/usr/bin/env python3
"""This file is the main entry point for the game."""
import traceback

import tcod

import color
import exceptions
import setup_game
import input_handlers


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it.
    
    This function is responsible for saving the game state to a file.
    It checks if the current event handler is an instance of EventHandler,
    which would mean the game is currently being played and there is an active
    Engine to save. The actual saving is delegated to the Engine's save_as method.
    """
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    """The main function of the game.
    
    This function is responsible for setting up the game window, loading the
    tileset, and running the main game loop. It also handles exceptions and
    ensures the game is saved on exit.
    """
    screen_width = 80
    screen_height = 50

    # Load the tileset used for rendering the game.
    tileset = tcod.tileset.load_tilesheet(
        "characters-320x80.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # The initial event handler is the main menu.
    # This handler is responsible for displaying the main menu and handling
    # user input on the menu. It will be replaced by the main game event
    # handler when the user starts a new game or loads a saved game.
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    # Create the main game window.
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="True Text RPG",
        vsync=True,
    ) as context:
        # The root console is the main surface where the game is rendered.
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            # This is the main game loop. It will run until the game is exited.
            while True:
                # Clear the console before rendering the next frame.
                root_console.clear()
                # Render the current game state to the console.
                # The on_render method is responsible for drawing the game map,
                # entities, and UI elements.
                handler.on_render(console=root_console)
                # Display the rendered console on the screen.
                context.present(root_console)

                try:
                    # Wait for the next event (e.g., key press, mouse move).
                    for event in tcod.event.wait():
                        # Convert the event to a format that the game can understand.
                        context.convert_event(event)
                        # Handle the event and update the game state.
                        # The handle_events method returns a new event handler,
                        # which allows for changing the game state (e.g., from
                        # the main menu to the game).
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            # If the user quits without saving, we just exit the game.
            raise
        except SystemExit:  # Save and quit.
            # If the user quits the game, we save the game before exiting.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            # If any other unexpected exception occurs, we save the game
            # before exiting to prevent losing progress.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
