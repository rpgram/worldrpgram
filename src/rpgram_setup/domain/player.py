import dataclasses

from rpgram_setup.domain.economics import Balance
from rpgram_setup.domain.heroes import PlayersHero, Good
from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass
class Player:
    balance: Balance
    inventory: list[Good]
    heroes: list[PlayersHero]
    username: str
    player_id: PlayerId

    def buy(self, item: Good) -> None:
        self.balance -= item.price
        self.inventory.append(item)

    def sell(self, item: Good) -> None:
        self.inventory.remove(item)
        self.balance += item.price
