import dataclasses

import aiohttp

from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.domain.gateways import RequestData
from rpgram_setup.domain.heroes import HeroClass
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import ClientProto, ConnectorProto
from rpgram_setup.domain.user_types import B, T, BattleId
from rpgram_setup.infrastructure.converters import player_to_dto_converter
from rpgram_setup.infrastructure.exceptions import BadRequest
from rpgram_setup.infrastructure.models import StartBattlePlayerDTO


class SessionManager(ConnectorProto[RequestData[T], T]):

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def make_call(self, call_data: RequestData[T]) -> T:
        self._refresh()
        async with self.session.request(
            call_data.method,
            call_data.api_url,
            json=call_data.body,
            params=call_data.query_params,
        ) as req:
            if 200 <= req.status < 300:
                data = await req.json()
            else:
                raise BadRequest(
                    call_data.api_url,
                    f"{req.status} - {(await req.content.read()).decode()}",
                )
        if dataclasses.is_dataclass(call_data.return_type):
            return call_data.return_type(**data)
        return call_data.return_type(data)

    def _refresh(self):
        pass


class BattleAPIClient(ClientProto):
    def __init__(
        self,
        manager: ConnectorProto[RequestData[BattleId], BattleId],
        config: AppConfig,
    ):
        self._connector = manager
        self._url = config.battle_url

    async def start_battle(
        self, player: Player, opponent: Player, hero_class: HeroClass
    ) -> BattleId:
        rd = RequestData(
            "POST",
            f"{self._url}/battle/instant",
            None,
            {
                "player": dataclasses.asdict(
                    player_to_dto_converter(player, hero_class)
                ),
                "opponent": dataclasses.asdict(
                    player_to_dto_converter(opponent, hero_class)
                ),
            },
            BattleId,
        )
        return await self._connector.make_call(rd)