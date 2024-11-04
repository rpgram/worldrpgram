import abc
from typing import Protocol

from rpgram_setup.domain.economics import Money
from rpgram_setup.domain.heroes import HeroClass
from rpgram_setup.domain.items import Equipment, Good
from rpgram_setup.domain.user_types import MinMax


class BattleUnit:
    """Passed to battle runtime."""


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
