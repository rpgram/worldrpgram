import asyncio
import dataclasses
import json
from typing import Any

import aio_pika
from aio_pika import Channel
from aio_pika.abc import AbstractRobustChannel

from rpgram_setup.domain.core import ConnectorProto, I, O, ClientProto


@dataclasses.dataclass
class RabbitCall:
    routing_key: str
    data: dict[str, Any]


class RabbitConnector(ConnectorProto[RabbitCall, None]):
    def __init__(self, channel: AbstractRobustChannel):
        self._channel = channel

    async def make_call(self, call_data: RabbitCall) -> None:
        await self._channel.default_exchange.publish(
            aio_pika.Message(json.dumps(call_data.data).encode()),
            routing_key=call_data.routing_key,
        )


class Client(ClientProto):
    def __init__(self, connector: RabbitConnector):
        self.connector = connector

    async def start_battle(self, player, opponent) -> None:
        dto = RabbitCall(
            "starts",
            {
                "player": dataclasses.asdict(player),
                "opponent": dataclasses.asdict(opponent),
            },
        )
        await self.connector.make_call(dto)


@dataclasses.dataclass
class StartBattleHeroDTO:
    health: int
    combo_root_id: int


@dataclasses.dataclass
class StartBattlePlayerDTO:
    name: str
    player_id: int
    hero: StartBattleHeroDTO


async def runs_start():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:

        channel = await connection.channel()
        rc = RabbitConnector(channel)
        c = Client(rc)
        await c.start_battle(
            StartBattlePlayerDTO("u", 1, StartBattleHeroDTO(2, 1)),
            StartBattlePlayerDTO("x", 3, StartBattleHeroDTO(2, 1)),
        )


if __name__ == "__main__":
    asyncio.run(runs_start())
