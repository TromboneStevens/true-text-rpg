"""This module contains the Inventory component."""
from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    """An entity component that handles an inventory of items."""

    parent: Actor

    def __init__(self, capacity: int):
        """Initializes the inventory."""
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """Remove an item from the inventory and drop it on the ground."""
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")
