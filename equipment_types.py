"""This module contains the EquipmentType enum."""
from enum import auto, Enum


class EquipmentType(Enum):
    """An enum for the different types of equipment."""

    WEAPON = auto()
    ARMOR = auto()
