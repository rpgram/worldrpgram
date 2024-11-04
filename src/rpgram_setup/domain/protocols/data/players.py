import abc
import dataclasses
from typing import Protocol, Any

from rpgram_setup.domain.player import Player
from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass
class GetPlayerQuery:
    player_id: PlayerId | None
    username: str | None


@dataclasses.dataclass
class CreatePlayer:
    username: str


class PlayersMapper(Protocol):
    db: Any

    @abc.abstractmethod
    def add_player(self, player: CreatePlayer) -> PlayerId: ...

    @abc.abstractmethod
    def get_player(self, query: GetPlayerQuery) -> Player | None: ...

    def _generate_id(self) -> PlayerId:
        """Mock, sometimes can be not implemented"""
        return PlayerId(0)

    @abc.abstractmethod
    def get_players(self) -> list[Player]: ...
