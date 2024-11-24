import dataclasses
from enum import IntEnum

from rpgram_setup.domain.economics import Money


@dataclasses.dataclass
class HeroStats:
    health: int
    armor: int
    damage: int


class HeroClass(IntEnum):
    WARRIOR = 1
    SORCERER = 2


@dataclasses.dataclass(frozen=True)
class Good:
    price_per_unit: Money
    name: str


@dataclasses.dataclass(frozen=True)
class Equipment(Good):
    """Grants characteristics by wearing, can be taken from somewhere."""

    class_: HeroClass
    stats_diff: HeroStats
    required_level: int


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
