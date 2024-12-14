import abc
import logging
from typing import Protocol, cast

from rpgram_setup.application.identity import IDProvider
from rpgram_setup.domain.battle import WaitingBattle
from rpgram_setup.domain.exceptions import NotUniqueError, SomethingIsMissingError
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.battle import WaitingBattleGatewayProto
from rpgram_setup.domain.protocols.data.players import GetPlayerQuery, PlayersMapper
from rpgram_setup.domain.user_types import PlayerId
from rpgram_setup.domain.vos.in_game import HeroClass

logger = logging.getLogger(__name__)


class WaitingBattleDTOReader(Protocol):
    @abc.abstractmethod
    def get_battles(self) -> list[WaitingBattle]: ...


class WaitForOpponentInteractor(Interactor[HeroClass, None]):
    def __init__(
        self,
        players: PlayersMapper,
        idp: IDProvider,
        waiters: WaitingBattleGatewayProto,
    ):
        self.waiters = waiters
        self.players = players
        self.idp = idp

    def execute(self, in_dto: HeroClass) -> None:
        self.idp.authenticated_only()
        player_id = cast(PlayerId, self.idp.get_payer_identity())
        player = self.players.get_player(GetPlayerQuery(player_id, None))
        if player is None:
            raise SomethingIsMissingError("Not matching identifier")
        try:
            next(h for h in player.heroes if h.born.class_ == in_dto)
        except StopIteration:
            raise SomethingIsMissingError("hero")
        if self.waiters.get_by_player(player_id):
            raise NotUniqueError("player_id waiting", player_id)
        self.waiters.insert_battle(WaitingBattle(player_id, in_dto))
        logger.info("Battle waiting from now", extra={"scope": "battle"})
