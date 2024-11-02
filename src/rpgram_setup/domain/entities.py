import abc
from dataclasses import dataclass
from enum import IntEnum
from typing import Protocol

from rpgram_setup.domain.economics import Money, Balance
from rpgram_setup.domain.exceptions import LevelTooLow, BattleContinues
from rpgram_setup.domain.items import Equipment, Good
from rpgram_setup.domain.user_types import MinMax


class BattleUnit:
    """Passed to battle runtime."""


@dataclass
class HeroStats:
    health: int
    armor: int
    damage: int


class HeroClass(IntEnum):
    WARRIOR = 1
    SORCERER = 2


class Hero:
    """Holds characteristics related to hero class. Can level up."""

    def __init__(self, hero_stats: HeroStats, level: int, class_: HeroClass):
        self.class_ = class_
        self.level = level
        self.hero_stats = hero_stats
        self.item: Equipment | None = None
        self.locked = False

    def _wear(self, item: Equipment) -> None:
        """Only items with same class are displayed."""
        if self.level < item.required_level:
            raise LevelTooLow
        self.hero_stats.armor += item.stats_diff.armor
        self.hero_stats.damage += item.stats_diff.damage
        self.hero_stats.health += item.stats_diff.health
        self.item = item

    def take_off(self) -> None:
        if self.locked:
            raise BattleContinues
        if self.item is None:
            return
        self.hero_stats.armor -= self.item.stats_diff.armor
        self.hero_stats.damage -= self.item.stats_diff.damage
        self.hero_stats.health -= self.item.stats_diff.health
        self.item = None

    def equip(self, item: Equipment) -> None:
        self.take_off()
        self._wear(item)


class Shop(Protocol):
    items: list[Equipment]

    @abc.abstractmethod
    def search(
        self,
        level: MinMax,
        price: MinMax,
        name_part: str | None = None,
        hero: HeroClass | None = None,
    ) -> list[Good]:
        """Returns matching items"""

    def put(self, item: Good) -> Money: ...

    def get(self, item: Good) -> Money: ...


class Player:
    def __init__(self, balance: Balance, inventory: list[Good], heroes: list[Hero]):
        self.inventory = inventory
        self.balance = balance
        self.heroes = heroes

    def buy(self, item: Good) -> None:
        self.balance -= item.price
        self.inventory.append(item)

    def sell(self, item: Good) -> None:
        self.inventory.remove(item)
        self.balance += item.price
