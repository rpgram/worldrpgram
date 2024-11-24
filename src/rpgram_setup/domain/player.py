import dataclasses

from rpgram_setup.domain.economics import Balance
from rpgram_setup.domain.entities import Slot
from rpgram_setup.domain.exceptions import ActionFailed
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.vos.in_game import Good
from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass
class Player:
    balance: Balance
    inventory: list[Slot]
    heroes: list[PlayersHero]
    username: str
    player_id: PlayerId

    def buy(self, item: Good, quantity: int = 1) -> None:
        max_slot_id = 0
        for s in self.inventory:
            if s.item.name == item.name:
                self.balance -= item.price_per_unit.mul(quantity, rize=True)
                s.quantity += quantity
                break
            if not max_slot_id:
                max_slot_id = s.slot_id
            elif max_slot_id < s.slot_id:
                max_slot_id = s.slot_id
        else:
            self.balance -= item.price_per_unit
            self.inventory.append(Slot(max_slot_id + 1, item, quantity))


    def sell(self, slot_id: int, quantity: int = 1) -> None:
        for s in self.inventory:
            if s.slot_id != slot_id:
                continue
            if quantity > s.quantity:
                raise ActionFailed
            if quantity == s.quantity:
                self.inventory.remove(s)
            else:
                s.quantity -= quantity
            self.balance += s.item.price_per_unit.mul(quantity, rize=False)
            break
