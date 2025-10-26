from __future__ import annotations

from typing import TYPE_CHECKING

import actions
import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


class ToggleAIAction(actions.Action):
    """An action that toggles the AI on and off."""

    def __init__(self, entity: Actor):
        """Initializes the toggle AI action."""
        super().__init__(entity)

    def perform(self) -> None:
        """Perform the toggle AI action."""
        self.engine.ai_enabled = not self.engine.ai_enabled
        if self.engine.ai_enabled:
            self.engine.message_log.add_message("AI enabled.", color.white)
        else:
            self.engine.message_log.add_message("AI disabled.", color.white)
