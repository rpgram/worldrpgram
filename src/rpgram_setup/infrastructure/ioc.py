from dishka import Provider, Scope, provide

from rpgram_setup.application.register import NewPlayerInteractor
from rpgram_setup.domain.protocols.data.players import PlayersMapper
from rpgram_setup.infrastructure.mappers import PlayerMemoryMapper


class InteractorProvider(Provider):

    scope = Scope.REQUEST

    player_mapper = provide(source=PlayerMemoryMapper, provides=PlayersMapper)
    register_interactor = provide(NewPlayerInteractor)
