import pytest
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from rpgram_setup.application.auth import (
    UserLoginDTO,
    UserLoginInteractor,
    UserRegisterDTO,
    UserRegisterInteractor,
)
from rpgram_setup.application.identity import SessionManager
from rpgram_setup.application.players.read import (
    ReadPlayerInteractor,
    ReadPlayersInteractor,
)
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.battle import UserMapper
from rpgram_setup.domain.protocols.data.players import (
    GetPlayerQuery,
    GetPlayersQuery,
    PlayersMapper,
)
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user import User

from ..stubs import HasherStub, MStub, PlayersMapperStub, UserMapperStub


class FakeProvider(Provider):
    scope = Scope.APP
    player_mapper = provide(PlayersMapperStub, provides=PlayersMapper)
    user_mapper = provide(UserMapperStub, provides=UserMapper)
    hasher = provide(HasherStub, provides=Hasher)
    idm = provide(MStub, provides=SessionManager)


class InteractorProvider(Provider):
    scope = Scope.APP
    get_players = provide(
        ReadPlayersInteractor, provides=Interactor[GetPlayersQuery, list[Player]]
    )
    get_player = provide(
        ReadPlayerInteractor, provides=Interactor[GetPlayerQuery, Player]
    )
    register_user = provide(
        UserRegisterInteractor, provides=Interactor[UserRegisterDTO, User]
    )
    login_user = provide(UserLoginInteractor, provides=Interactor[UserLoginDTO, User])


@pytest.fixture(scope="session")
def async_cont() -> AsyncContainer:
    return make_async_container(FakeProvider(), InteractorProvider())
