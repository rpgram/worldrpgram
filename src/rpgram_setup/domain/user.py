import dataclasses
from typing import Callable, TypeVar, Generic

from rpgram_setup.domain.user_types import PlayerId


S = TypeVar("S")


class Sensitive(Generic[S]):
    def __init__(self, value: S) -> None:
        self.value = value

    def __str__(self) -> str:
        return "*" * 16

    def __repr__(self) -> str:
        return "*" * 16


@dataclasses.dataclass
class User:
    player_id: PlayerId
    login: str
    password_hash: str
    telegram_id: int | None = None

    def check_password(self, password: str, hasher: Callable[[str], str]):
        return hasher(password) == self.password_hash

    def get_telegram_link(self) -> str:
        raise NotImplementedError
