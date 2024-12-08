import dataclasses

from rpgram_setup.domain.user_types import PlayerId
from rpgram_setup.domain.vos.in_game import HeroClass


@dataclasses.dataclass(frozen=True, slots=True)
class UserDTO:
    login: str


@dataclasses.dataclass
class GoodDTO:
    price: list[str]
    name: str


@dataclasses.dataclass
class SlotDTO:
    item: GoodDTO
    quantity: int
    slot_id: int


@dataclasses.dataclass
class HeroDTO:
    level: int
    health: int
    hero_class: HeroClass
    equipment: str | None


@dataclasses.dataclass
class PlayerDTO:
    balance: str
    inventory: list[SlotDTO]
    heroes: list[HeroClass]
    username: str
    player_id: PlayerId
