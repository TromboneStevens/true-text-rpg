"""This module contains the RenderOrder enum."""
from enum import auto, Enum


class RenderOrder(Enum):
    """An enum for the render order of entities."""

    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
