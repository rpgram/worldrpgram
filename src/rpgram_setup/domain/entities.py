import abc
import dataclasses

from rpgram_setup.domain.economics import Money
from rpgram_setup.domain.exceptions import ActionFailed
from rpgram_setup.domain.vos.in_game import HeroClass, Good, Equipment
from rpgram_setup.domain.user_types import MinMax, MinMaxMoney


@dataclasses.dataclass
class Slot:
    slot_id: int
    item: Good
    quantity: int


class BattleUnit:
    """Passed to battle runtime."""


class Shop(abc.ABC):
    _shelf: list[Good]

    def search(
        self,
        level: MinMax,
        price: MinMaxMoney,
        name: str | None = None,
        hero: HeroClass | None = None,
    ) -> list[Good]:
        """Returns matching items"""
        result = []
        for s in self._shelf:
            price_ok = price[0] <= s.price_per_unit <= price[1]
            level_ok = not isinstance(s, Equipment) or (
                (level[0] is None or level[0] <= s.required_level)
                and (level[1] is None or s.required_level <= level[1])
            )
            name_ok = not name or name == s.name
            hero_ok = not hero or not isinstance(s, Equipment) or s.class_ == hero
            if price_ok and level_ok and name_ok and hero_ok:
                result.append(s)
        return result

    @abc.abstractmethod
    def put(self, item: Good, quantity: int) -> Money: ...

    @abc.abstractmethod
    def get(self, item: Good, quantity: int) -> Money: ...


class CentralShop(Shop):

    def __init__(self, shelf: list[Good]):
        self._shelf = shelf

    def _check_availability(self, item: Good):
        for g in self._shelf:
            if g.name == item.name:
                break
        else:
            raise ActionFailed

    def put(self, item: Good, quantity: int) -> Money:
        self._check_availability(item)
        return item.price_per_unit.mul(quantity, rize=False)

    def get(self, item: Good, quantity: int) -> Money:
        self._check_availability(item)
        return item.price_per_unit.mul(quantity, rize=True)
