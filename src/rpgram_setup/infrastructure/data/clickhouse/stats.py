import time
import uuid
from collections import defaultdict
from typing import Mapping

from asynch import Connection  # type: ignore[import-untyped]

from . import models
from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.data.statisctics import (
    StatisticsWriter,
    TradeEvent,
    AnalyticsBatcher,
    T,
)


class ClickHouseBatcher(AnalyticsBatcher):
    def __init__(self, connection: Connection):
        self.connection = connection
        self.tables_with_data: defaultdict[type[Mapping], list[Mapping]] = defaultdict(
            list
        )

    def add_one(self, table: type[T], record: T) -> None:
        self.tables_with_data[table].append(record)

    async def _flush_battle_result(self, data: list[Mapping]):
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO battle_results (
                    battle_id,
                    start_timestamp,
                    end_timestamp,
                    opponent_id,
                    player_id,
                    timeout,
                    winner_id
                ) VALUES
                """,
                data,
            )

    async def _flush_trade_results(self, data: list[Mapping]):
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO trade (
                    id,
                    timestamp,
                    token_units,
                    good_name,
                    quantity,
                    buy
                ) VALUES
                """,
                data,
            )

    async def _flush_table(self, table: type[Mapping]) -> None:
        data = self.tables_with_data.get(table)
        if not data:
            return
        if table is models.BattleResult:
            await self._flush_battle_result(data)
            self.tables_with_data[models.BattleResult] = []
        elif table is models.Trade:
            await self._flush_trade_results(data)
            self.tables_with_data[models.Trade] = []

    async def flush_all(self) -> None:
        for t in self.tables_with_data:
            await self._flush_table(t)


class AnalyticsWriteRepository(StatisticsWriter):
    def __init__(self, batcher: AnalyticsBatcher):
        self._batcher = batcher

    async def trade(self, event: TradeEvent) -> None:
        current_ts = time.time()
        record = {
            "timestamp": current_ts,
            "token_units": event.item.price_per_unit.units,
            "id": uuid.uuid4(),
            "good_name": event.item.name,
            "quantity": event.quantity,
            "buy": event.purchase,
        }
        self._batcher.add_one(models.Trade, record)

    async def save_battle_result(self, battle_result: BattleResult) -> None:
        current_ts = time.time()
        player_wins = battle_result.hero_result.win
        record = {
            "battle_id": battle_result.battle_id,
            "start_timestamp": None,
            "end_timestamp": current_ts,
            "opponent_id": battle_result.opponent_result.player_id,
            "player_id": battle_result.hero_result.player_id,
            "timeout": player_wins and battle_result.opponent_result.win,
            "winner_id": (
                battle_result.hero_result.player_id
                if player_wins
                else battle_result.opponent_result.player_id
            ),
        }
        self._batcher.add_one(models.BattleResult, record)
