import abc
from typing import Protocol, TypeVar

from rpgram_setup.domain.economics import Token
from rpgram_setup.domain.entities import CentralShop, Shop
from rpgram_setup.domain.protocols.core import ShopFactory
from rpgram_setup.domain.vos.in_game import Equipment, Good, Hero, HeroClass, HeroStats


class HeroFactory:

    def create_warrior(self) -> Hero:
        hero_stats = HeroStats(10, 13, 25)
        per_level = HeroStats(10, 1, 2)
        return Hero(hero_stats, per_level, HeroClass.WARRIOR, None)

    def create_sorcerer(self) -> Hero:
        hero_stats = HeroStats(25, 5, 20)
        per_level = HeroStats(10, 1, 3)
        return Hero(hero_stats, per_level, HeroClass.SORCERER, None)


Ingredients = TypeVar("Ingredients", contravariant=True)
TargetItem = TypeVar("TargetItem", covariant=True, bound=Good)


class ItemFactory(Protocol[TargetItem, Ingredients]):

    @abc.abstractmethod
    def create_item(self, ingredients: Ingredients) -> TargetItem:
        """Returns quantity of created items"""


class NullSuiteFactory(ItemFactory[Equipment, None]):
    def create_item(self, ingredients: None) -> Equipment:
        stats_diff = HeroStats(5, 1, 0)
        return Equipment(Token(5), "Null Suite", HeroClass.WARRIOR, stats_diff, 0)


class CentralShopFactory(ShopFactory):
    def __init__(self, ns_factory: NullSuiteFactory):
        self.factories = [ns_factory]

    def create_shop(self) -> Shop:
        return CentralShop([f.create_item(None) for f in self.factories])
