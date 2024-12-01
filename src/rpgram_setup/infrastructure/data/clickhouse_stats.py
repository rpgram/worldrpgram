import time
import uuid

from asynch import Cursor

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
            ) VALUES""",
            [
                {
                    "timestamp": current_ts,
                    "token_units": event.item.price_per_unit.units,
                    "id": uuid.uuid4(),
                    "good_name": event.item.name,
                    "quantity": event.quantity,
                    "buy": event.purchase,
                }
            ],
        )
