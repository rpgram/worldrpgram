import abc
import dataclasses
from typing import Protocol

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
