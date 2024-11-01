import abc
from dataclasses import dataclass
from enum import IntEnum
from typing import Protocol, Final

from rpgram_setup.domain.economics import Money, Balance
from rpgram_setup.domain.exceptions import LevelTooLow
from rpgram_setup.domain.user_types import Ledger, MinMax


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


class Item:
    """Grants characteristics by wearing, can be taken from somewhere."""

    def __init__(
        self, hero_stats: HeroStats, price: Money, level: int, class_: HeroClass
    ):
        self.class_ = class_
        self.stats_diff = hero_stats
        self.price = price
        self.required_level = level


class Hero:
    """Holds characteristics related to hero class. Can level up."""

    def __init__(self, hero_stats: HeroStats, level: int, class_: HeroClass):
        self.class_ = class_
        self.level = level
        self.hero_stats = hero_stats
        self.item: Item | None = None

    def _wear(self, item: Item):
        """Only items with same class are displayed."""
        if self.level < item.required_level:
            raise LevelTooLow
        self.hero_stats.armor += item.stats_diff.armor
        self.hero_stats.damage += item.stats_diff.damage
        self.hero_stats.health += item.stats_diff.health
        self.item = item

    def take_off(self):
        if self.item is None:
            return
        self.hero_stats.armor -= self.item.stats_diff.armor
        self.hero_stats.damage -= self.item.stats_diff.damage
        self.hero_stats.health -= self.item.stats_diff.health
        self.item = None

    def equip(self, item: Item):
        self.take_off()
        self._wear(item)


class Shop(Protocol):
    items: list[Item]

    @abc.abstractmethod
    def search(
        self,
        level: MinMax,
        price: MinMax,
        name_part: str | None = None,
        hero: HeroClass | None = None,
    ) -> list[Item]:
        """Returns matching items"""

    def put(self, item: Item) -> Money: ...

    def get(self, item: Item) -> Money: ...


class Player:
    def __init__(self, balance: Balance, inventory: list[Item], heroes: list[Hero]):
        self.inventory = inventory
        self.balance = balance
        self.heroes = heroes

    def buy(self, item: Item):
        self.balance -= item.price
        self.inventory.append(item)

    def sell(self, item: Item):
        self.inventory.remove(item)
        self.balance += item.price
