import dataclasses
from typing import Protocol, TYPE_CHECKING

from rpgram_setup.domain.economics import Money

if TYPE_CHECKING:
    from rpgram_setup.domain.heroes import HeroStats, HeroClass


@dataclasses.dataclass
class Good:
    price: Money
    quantity: int
    name: str


class Equipment(Good):
    """Grants characteristics by wearing, can be taken from somewhere."""

    quantity = 1

    def __init__(
        self,
        hero_stats: "HeroStats",
        price: Money,
        level: int,
        class_: "HeroClass",
        name: str,
    ):
        self.name = name
        self.class_ = class_
        self.stats_diff = hero_stats
        self.price = price
        self.required_level = level
