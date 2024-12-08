import time
import uuid

from asynch import Cursor  # type: ignore[import-untyped]

from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.data.statisctics import StatisticsWriter, TradeEvent


class ClickHouseWriter(StatisticsWriter):
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def trade(self, event: TradeEvent) -> None:
        current_ts = time.time()
        await self._cursor.execute(
            """INSERT INTO trade  (
                `id`,
                `timestamp`,
                `token_units`,
                `good_name`,
                `quantity`,
                `buy`
            ) VALUES (generateUUIDv4(), %(timestamp)s, %(token_units)s, %(good_name)s, %(quantity)s, %(buy)s)""",
            {
                "timestamp": current_ts,
                "token_units": event.item.price_per_unit.units,
                "id": uuid.uuid4(),
                "good_name": event.item.name,
                "quantity": event.quantity,
                "buy": event.purchase,
            },
        )

    async def save_battle_result(self, battle_result: BattleResult) -> None:
        current_ts = time.time()
        player_wins = battle_result.hero_result.win
        await self._cursor.execute(
            """INSERT INTO battle_results (
                battle_id,
                start_timestamp,
                end_timestamp,
                opponent_id,
                player_id,
                timeout,
                winner_id
            ) VALUES
            """,
            [
                {
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
            ],
        )
