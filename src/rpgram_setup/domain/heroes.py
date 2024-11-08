import dataclasses
from enum import IntEnum

from rpgram_setup.domain.exceptions import LevelTooLow, BattleContinues
from rpgram_setup.domain.items import Equipment


@dataclasses.dataclass
class HeroStats:
    health: int
    armor: int
    damage: int


class HeroClass(IntEnum):
    WARRIOR = 1
    SORCERER = 2


@dataclasses.dataclass
class Hero:
    default_stats: HeroStats
    per_level_stats: HeroStats
    class_: HeroClass
    equipment: Equipment | None = None

    def level_up(self, hero_stats: HeroStats):
        hero_stats.armor += self.per_level_stats.armor
        hero_stats.health += self.per_level_stats.health
        hero_stats.damage += self.per_level_stats.damage


class PlayersHero:
    """Holds characteristics related to hero class. Can level up."""

    def __init__(self, hero: Hero):
        self.hero = hero
        self.hero_stats = hero.default_stats
        self.item: Equipment | None = hero.equipment
        self.locked = False
        self.level = 1

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

    def level_up(self):
        self.hero.level_up(self.hero_stats)
