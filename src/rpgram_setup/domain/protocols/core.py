import abc
from typing import Protocol, TypeVar, Any

from rpgram_setup.domain.entities import Shop
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.infrastructure.models import BattleStarted

Input = TypeVar("Input", bound=Any, contravariant=True)
Output = TypeVar("Output", bound=Any, covariant=True)


class ConnectorProto(Protocol[Input, Output]):
    @abc.abstractmethod
    async def make_call(self, call_data: Input) -> Output: ...


I = TypeVar("I")  # noqa: E741
O = TypeVar("O")  # noqa: E741


class ClientProto(Protocol[I, O]):
    _connector: ConnectorProto[I, O]

    @abc.abstractmethod
    async def start_battle(
        self,
        player: Player,
        opponent: Player,
        players_hero: PlayersHero,
        opponents_hero: PlayersHero,
    ) -> BattleStarted: ...


SyncInteractorInput = TypeVar("SyncInteractorInput", bound=Any, contravariant=True)
SyncInteractorOutput = TypeVar("SyncInteractorOutput", bound=Any, covariant=True)


class Interactor(Protocol[SyncInteractorInput, SyncInteractorOutput]):
    @abc.abstractmethod
    def execute(self, in_dto: SyncInteractorInput) -> SyncInteractorOutput: ...


AsyncInteractorInput = TypeVar("AsyncInteractorInput", bound=Any, contravariant=True)
AsyncInteractorOutput = TypeVar("AsyncInteractorOutput", bound=Any, covariant=True)


class AsyncInteractor(Protocol[AsyncInteractorInput, AsyncInteractorOutput]):
    @abc.abstractmethod
    async def execute(self, in_dto: AsyncInteractorInput) -> AsyncInteractorOutput: ...


class ShopFactory(Protocol):
    @abc.abstractmethod
    def create_shop(self) -> Shop: ...
