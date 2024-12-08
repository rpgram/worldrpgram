from rpgram_setup.application.identity import SessionManager
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.data.battle import UserMapper
from rpgram_setup.domain.protocols.data.players import (
    PlayersMapper,
    GetPlayersQuery,
    CreatePlayer,
    GetPlayerQuery,
)
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import PlayerId
from .data import FAKE_PLAYER, FAKE_USER, NEW_LOGIN, HASH


class PlayersMapperStub(PlayersMapper):
    def get_player(self, query: GetPlayerQuery) -> Player | None:
        return FAKE_PLAYER

    def add_player(self, player: CreatePlayer) -> PlayerId:
        pass

    def get_players(self, query: GetPlayersQuery) -> list[Player]:
        return [FAKE_PLAYER]


class UserMapperStub(UserMapper):
    def insert_user(self, user: User):
        pass

    def get_user(self, login: str) -> User | None:
        if login == NEW_LOGIN:
            return None
        return FAKE_USER


class HasherStub(Hasher):
    def hash(self, value: str) -> str:
        return HASH


class MStub(SessionManager):
    __cookie_key__: str = "RSESSION_ID"

    def assign_session(self, player_id: PlayerId):
        pass

    def refresh_session(self, old_session: str | None):
        pass
