import abc
import dataclasses
from typing import Protocol, TypeVar, Mapping, Any

from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.economics import Money
from rpgram_setup.domain.vos.in_game import Good


@dataclasses.dataclass(frozen=True)
class TradeEvent:
    purchase: bool
    item: Good
    quantity: int
    paid: Money


class StatisticsWriter(Protocol):
    @abc.abstractmethod
    async def trade(self, event: TradeEvent) -> None: ...

    @abc.abstractmethod
    async def save_battle_result(self, battle_result: BattleResult) -> None: ...


T = TypeVar("T", bound=Mapping[str, Any])


class AnalyticsBatcher(Protocol):
    @abc.abstractmethod
    def add_one(self, table: type[T], record: T) -> None: ...

    @abc.abstractmethod
    async def _flush_table(self, table: type[Mapping[str, Any]]) -> None: ...

    @abc.abstractmethod
    async def flush_all(self) -> None: ...
