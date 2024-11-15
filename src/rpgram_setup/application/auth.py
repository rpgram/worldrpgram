import dataclasses
from typing import Callable

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.application.identity import RSessionIDManager
from rpgram_setup.domain.exceptions import NotUnique, ActionFailed
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor, I, O
from rpgram_setup.domain.protocols.data.battle import UserMapper
from rpgram_setup.domain.protocols.data.players import (
    PlayersMapper,
    GetPlayerQuery,
    CreatePlayer,
)
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass
class UserLoginDTO:
    login: str
    password: str


@dataclasses.dataclass
class UserRegisterDTO(UserLoginDTO):
    username: str


class UserLoginInteractor(Interactor[UserLoginDTO, User]):

    def __init__(
        self,
        user_getter: UserMapper,
        idm: RSessionIDManager,
        hasher: Callable[[str], str],
    ):
        self.hasher = hasher
        self.idm = idm
        self.user_getter = user_getter

    def execute(self, in_dto: UserLoginDTO) -> User:
        user = self.user_getter.get_user(in_dto.login)
        if user is None:
            raise NotAuthenticated
        if not user.check_password(in_dto.password, self.hasher):
            raise NotAuthenticated
        self.idm.login(user.player_id)
        return user


class UserRegisterInteractor(Interactor[UserRegisterDTO, User]):
    def __init__(
        self,
        user_getter: UserMapper,
        players_mapper: PlayersMapper,
        idm: RSessionIDManager,
        hasher: Callable[[str], str],
    ):
        self.hasher = hasher
        self.players_mapper = players_mapper
        self.idm = idm
        self.user_mapper = user_getter

    def execute(self, in_dto: UserRegisterDTO) -> User:
        conflict = self.user_mapper.get_user(in_dto.login)
        if conflict is not None:
            raise NotUnique("login", in_dto.login)
        player_id = self.players_mapper.add_player(CreatePlayer(in_dto.username))
        password_hash = self.hasher(in_dto.password)
        user = User(player_id, in_dto.login, password_hash)
        self.user_mapper.insert_user(user)
        return user
