import abc
from typing import Any, Protocol, TypeVar

from rpgram_setup.domain.entities import Shop
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.infrastructure.models import BattleStarted

I = TypeVar("I", bound=Any, contravariant=True)
O = TypeVar("O", bound=Any, covariant=True)


class ConnectorProto(Protocol[I, O]):
    @abc.abstractmethod
    async def make_call(self, call_data: I) -> O: ...


class ClientProto(Protocol):
    _connector: ConnectorProto

    @abc.abstractmethod
    async def start_battle(
        self,
        player: Player,
        opponent: Player,
        players_hero: PlayersHero,
        opponents_hero: PlayersHero,
    ) -> BattleStarted: ...


class Interactor(Protocol[I, O]):

    @abc.abstractmethod
    def execute(self, in_dto: I) -> O: ...


class AsyncInteractor(Protocol[I, O]):

    @abc.abstractmethod
    async def execute(self, in_dto: I) -> O: ...


class ShopFactory(Protocol):

    @abc.abstractmethod
    def create_shop(self) -> Shop: ...
