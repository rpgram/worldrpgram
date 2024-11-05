from dishka import Provider, Scope, provide, make_async_container, AsyncContainer

from rpgram_setup.application.players.read import (
    ReadPlayersInteractor,
    ReadPlayerInteractor,
)
from rpgram_setup.application.players.register import NewPlayerInteractor
from rpgram_setup.domain.protocols.data.players import PlayersMapper
from rpgram_setup.infrastructure.mappers import PlayerMemoryMapper


class InteractorProvider(Provider):

    scope = Scope.REQUEST

    player_mapper = provide(
        source=PlayerMemoryMapper, provides=PlayersMapper, scope=Scope.APP
    )
    register_interactor = provide(NewPlayerInteractor)
    get_all_interactor = provide(ReadPlayersInteractor)
    get_interactor = provide(ReadPlayerInteractor)


def make_container() -> AsyncContainer:
    return make_async_container(InteractorProvider())
