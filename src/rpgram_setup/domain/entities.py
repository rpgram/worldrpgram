import abc
from typing import Protocol

from rpgram_setup.domain.economics import Money, Balance
from rpgram_setup.domain.heroes import HeroClass, PlayersHero
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


class Player:
    def __init__(
        self,
        balance: Balance,
        inventory: list[Good],
        heroes: list[PlayersHero],
        username: str,
        player_id: int,
    ):
        self.player_id = player_id
        self.username = username
        self.inventory = inventory
        self.balance = balance
        self.heroes = heroes

    def buy(self, item: Good) -> None:
        self.balance -= item.price
        self.inventory.append(item)

    def sell(self, item: Good) -> None:
        self.inventory.remove(item)
        self.balance += item.price
