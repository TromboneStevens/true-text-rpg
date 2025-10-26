"""This module contains the main Engine class for the game."""
from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING, Tuple

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    """The main engine of the game.

    This class is responsible for managing the game state, including the game map,
    the player, and the message log. It also handles enemy turns, updates the
    field of view, and renders the game to the console.
    """

    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        """Initialize the Engine.

        Args:
            player: The player actor.
        """
        self.message_log = MessageLog()
        self.mouse_location: Tuple[int, int] = (0, 0)
        self.player = player
        self.ai_enabled = True

    def handle_enemy_turns(self) -> None:
        """Handle the turns of all enemies on the current game map."""
        if not self.ai_enabled:
            return
        # We iterate over a copy of the actors set, so we can modify it while iterating.
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    # Let the enemy perform its action.
                    entity.ai.perform()
                except exceptions.Impossible:
                    # Ignore impossible actions from AI.
                    pass

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        """Render the game to the console.

        This method is responsible for drawing the game map, the message log,
        the player's health bar, the current dungeon level, and the names of
        entities at the mouse location.

        Args:
            console: The console to render to.
        """
        # Render the game map.
        self.game_map.render(console)

        # Render the message log.
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        # Render the player's health bar.
        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        # Render the current dungeon level.
        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        # Render the names of entities at the mouse location.
        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
