import dataclasses
import logging

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.application.identity import RSessionIDManager
from rpgram_setup.domain.exceptions import NotUnique, ValidationError
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.battle import UserMapper
from rpgram_setup.domain.protocols.data.players import (
    PlayersMapper,
    CreatePlayer,
)
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user import User


@dataclasses.dataclass
class UserLoginDTO:
    login: str
    password: str


@dataclasses.dataclass
class UserRegisterDTO(UserLoginDTO):
    username: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.password) < 10:
            raise ValidationError("password", "at least 10 characters")
        if not (self.login and self.username):
            raise ValidationError("input", "non-empty only")


class UserLoginInteractor(Interactor[UserLoginDTO, User]):

    def __init__(
        self,
        user_getter: UserMapper,
        idm: RSessionIDManager,
        hasher: Hasher,
    ):
        self.hasher = hasher
        self.idm = idm
        self.user_getter = user_getter

    def execute(self, in_dto: UserLoginDTO) -> User:
        user = self.user_getter.get_user(in_dto.login)
        if user is None:
            raise NotAuthenticated
        if not user.check_password(in_dto.password, self.hasher.hash):
            raise NotAuthenticated
        self.idm.assign_session(user.player_id)
        return user


class UserRegisterInteractor(Interactor[UserRegisterDTO, User]):
    def __init__(
        self,
        user_getter: UserMapper,
        players_mapper: PlayersMapper,
        idm: RSessionIDManager,
        hasher: Hasher,
    ):
        self.hasher = hasher
        self.players_mapper = players_mapper
        self.idm = idm
        self.user_mapper = user_getter

    def execute(self, in_dto: UserRegisterDTO) -> User:
        conflict = self.user_mapper.get_user(in_dto.login)
        if conflict is not None:
            raise NotUnique("assign_session", in_dto.login)
        player_id = self.players_mapper.add_player(CreatePlayer(in_dto.username))
        password_hash = self.hasher.hash(in_dto.password)
        user = User(player_id, in_dto.login, password_hash)
        self.user_mapper.insert_user(user)
        logging.info("User %s for pid %s created", in_dto.login, player_id)
        self.idm.assign_session(player_id)
        return user
