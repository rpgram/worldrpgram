import pytest
from dishka import Provider, provide, make_async_container, AsyncContainer, Scope

from rpgram_setup.application.auth import (
    UserRegisterInteractor,
    UserRegisterDTO,
    UserLoginInteractor,
    UserLoginDTO,
)
from rpgram_setup.application.identity import SessionManager
from rpgram_setup.application.players.read import (
    ReadPlayersInteractor,
    ReadPlayerInteractor,
)
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.battle import UserMapper
from rpgram_setup.domain.protocols.data.players import (
    GetPlayersQuery,
    PlayersMapper,
    GetPlayerQuery,
)
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user import User
from ..stubs import PlayersMapperStub, UserMapperStub, HasherStub, MStub


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
