import dataclasses
import logging
from typing import cast

from rpgram_setup.application.identity import IDProvider
from rpgram_setup.domain.exceptions import ActionFailedError, SomethingIsMissingError
from rpgram_setup.domain.protocols.core import AsyncInteractor, ClientProto
from rpgram_setup.domain.protocols.data.battle import WaitingBattleGatewayProto
from rpgram_setup.domain.protocols.data.players import GetPlayerQuery, PlayersMapper
from rpgram_setup.domain.user_types import BattleId, PlayerId
from rpgram_setup.domain.vos.in_game import HeroClass
from rpgram_setup.infrastructure.data.gateways import BattleKeysGateway

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class StartBattleDTO:
    opponent_id: PlayerId
    hero_class: HeroClass | None


class StartBattleInteractor(AsyncInteractor[StartBattleDTO, BattleId]):
    def __init__(
        self,
        battlefield_gateway: ClientProto,
        player_data_mapper: PlayersMapper,
        battle_keys: BattleKeysGateway,
        waiters: WaitingBattleGatewayProto,
        idp: IDProvider,
    ):
        self.idp = idp
        self.waiters = waiters
        self.battle_keys = battle_keys
        self.player_data_mapper = player_data_mapper
        self.battlefield_gateway = battlefield_gateway

    async def execute(self, in_dto: StartBattleDTO) -> BattleId:
        self.idp.authenticated_only()
        player_id = cast(PlayerId, self.idp.get_payer_identity())
        if player_id == in_dto.opponent_id:
            logger.warning("Not to self!", extra={"scope": "battle"})
            raise ActionFailedError
        existing_battle = self.waiters.get_by_player(in_dto.opponent_id)
        if not existing_battle:
            logger.warning("No battle", extra={"scope": "battle"})
            raise ActionFailedError
        if in_dto.hero_class and in_dto.hero_class != existing_battle.hero_class:
            logger.warning("Hero choice conflict", extra={"scope": "battle"})
            raise ActionFailedError
        player = self.player_data_mapper.get_player(GetPlayerQuery(player_id, None))
        if player is None:
            raise SomethingIsMissingError("participant")
        opponent = self.player_data_mapper.get_player(
            GetPlayerQuery(in_dto.opponent_id, None)
        )
        if opponent is None:
            raise SomethingIsMissingError("opponent")
        try:
            players_hero = next(
                h for h in player.heroes if h.born.class_ == existing_battle.hero_class
            )
            opponents_hero = next(
                h
                for h in opponent.heroes
                if h.born.class_ == existing_battle.hero_class
            )
        except StopIteration:
            raise SomethingIsMissingError("hero")
        if self.waiters.get_by_player(player_id):
            self.waiters.remove_battle(player_id)
        battle_started = await self.battlefield_gateway.start_battle(
            player, opponent, players_hero, opponents_hero
        )
        self.battle_keys.add_key(player.player_id, battle_started.player_key)
        self.battle_keys.add_key(opponent.player_id, battle_started.opponent_key)
        logger.info(
            "Keys for %s and %s saved",
            player.player_id,
            opponent.player_id,
            extra={"scope": "iam"},
        )
        return battle_started.battle_id
