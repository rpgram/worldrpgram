import dataclasses

from rpgram_setup.domain.heroes import HeroClass
from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass(frozen=True, slots=True)
class UserDTO:
    login: str


@dataclasses.dataclass
class GoodDTO:
    price: list[str]
    quantity: int
    name: str


@dataclasses.dataclass
class HeroDTO:
    level: int
    health: int
    hero_class: HeroClass


@dataclasses.dataclass
class PlayerDTO:
    balance: str
    inventory: list[GoodDTO]
    heroes: list[HeroClass]
    username: str
    player_id: PlayerId
