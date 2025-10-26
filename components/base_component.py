"""This module contains the base class for all components."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    """A base class for all components.

    Attributes:
        parent (Entity): The owning entity instance.
    """

    parent: Entity  # Owning entity instance.

    @property
    def gamemap(self) -> GameMap:
        """Return the game map."""
        return self.parent.gamemap

    @property
    def engine(self) -> Engine:
        """Return the engine."""
        return self.gamemap.engine
