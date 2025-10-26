"""This module contains the Equippable component and its subclasses."""
from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    """An entity component that makes an item equippable."""

    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        """Initializes the equippable."""
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


class Dagger(Equippable):
    """A dagger."""

    def __init__(self) -> None:
        """Initializes the dagger."""
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)


class Sword(Equippable):
    """A sword."""

    def __init__(self) -> None:
        """Initializes the sword."""
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)


class LeatherArmor(Equippable):
    """Leather armor."""

    def __init__(self) -> None:
        """Initializes the leather armor."""
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class ChainMail(Equippable):
    """Chain mail."""

    def __init__(self) -> None:
        """Initializes the chain mail."""
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)
