import dataclasses
import logging

from rpgram_setup.domain.exceptions import SomethingIsMissingError
from rpgram_setup.domain.vos.in_game import HeroClass
from rpgram_setup.domain.protocols.core import (
    ClientProto,
    AsyncInteractor,
)
from rpgram_setup.domain.protocols.data.players import PlayersMapper, GetPlayerQuery
from rpgram_setup.domain.user_types import BattleId, PlayerId
from rpgram_setup.infrastructure.data.gateways import BattleKeysGateway

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class StartBattleDTO:
    player_id: PlayerId
    opponent_id: PlayerId
    hero_class: HeroClass


class StartBattleInteractor(AsyncInteractor[StartBattleDTO, BattleId]):
    def __init__(
        self,
        battlefield_gateway: ClientProto,
        player_data_mapper: PlayersMapper,
        battle_keys: BattleKeysGateway,
    ):
        self.battle_keys = battle_keys
        self.player_data_mapper = player_data_mapper
        self.battlefield_gateway = battlefield_gateway

    async def execute(self, in_dto: StartBattleDTO) -> BattleId:
        assert in_dto.player_id != in_dto.opponent_id
        player = self.player_data_mapper.get_player(
            GetPlayerQuery(in_dto.player_id, None)
        )
        if player is None:
            raise SomethingIsMissingError("participant")
        opponent = self.player_data_mapper.get_player(
            GetPlayerQuery(in_dto.opponent_id, None)
        )
        if opponent is None:
            raise SomethingIsMissingError("participant")
        try:
            players_hero = next(
                h for h in player.heroes if h.born.class_ == in_dto.hero_class
            )
            opponents_hero = next(
                h for h in opponent.heroes if h.born.class_ == in_dto.hero_class
            )
        except StopIteration:
            raise SomethingIsMissingError("hero")
        battle_started = await self.battlefield_gateway.start_battle(
            player, opponent, players_hero, opponents_hero
        )
        self.battle_keys.add_key(player.player_id, battle_started.player_key)
        self.battle_keys.add_key(opponent.player_id, battle_started.opponent_key)
        logger.info("Keys for %s and %s saved", player.player_id, opponent.player_id, extra={"scope":"iam"})
        return battle_started.battle_id
