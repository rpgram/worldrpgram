import dataclasses

import aiohttp

from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.domain.gateways import RequestData
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import ClientProto, ConnectorProto
from rpgram_setup.domain.user_types import T
from rpgram_setup.infrastructure.converters import player_to_dto_converter
from rpgram_setup.infrastructure.exceptions import BadRequest
from rpgram_setup.infrastructure.models import BattleStarted


class HTTPSessionManager(ConnectorProto[RequestData[T], T]):
    def __init__(self) -> None:
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
        if isinstance(call_data.return_type, type) and dataclasses.is_dataclass(
            call_data.return_type
        ):
            return call_data.return_type(**data)  # type:ignore[return-value]
        return call_data.return_type(data)  # type:ignore[call-arg]

    def _refresh(self) -> None:
        pass


class BattleAPIClient(ClientProto[RequestData[BattleStarted], BattleStarted]):
    def __init__(
        self,
        manager: ConnectorProto[RequestData[BattleStarted], BattleStarted],
        config: AppConfig,
    ):
        self._connector = manager
        self._url = config.battle_url

    async def start_battle(
        self,
        player: Player,
        opponent: Player,
        players_hero: PlayersHero,
        opponents_hero: PlayersHero,
    ) -> BattleStarted:
        rd = RequestData(
            "POST",
            f"{self._url}/battle/instant",
            None,
            {
                "player": dataclasses.asdict(
                    player_to_dto_converter(player, players_hero)
                ),
                "opponent": dataclasses.asdict(
                    player_to_dto_converter(opponent, opponents_hero)
                ),
            },
            BattleStarted,
        )
        return await self._connector.make_call(rd)
