import dataclasses
from typing import Callable

from rpgram_setup.domain.user_types import PlayerId


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
