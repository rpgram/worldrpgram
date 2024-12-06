from rpgram_setup.application.identity import (
    RSessionIDManager,
    IDProvider,
)
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.exceptions import ActionFailed
from rpgram_setup.domain.protocols.core import Interactor, I
from rpgram_setup.domain.protocols.data.players import (
    CreatePlayer,
    PlayersMapper,
    GetPlayerQuery,
)


class NewPlayerInteractor(Interactor[CreatePlayer, Player]):
    def __init__(
        self, player_mapper: PlayersMapper, idm: RSessionIDManager, idp: IDProvider
    ):
        self._idm = idm
        self._player_mapper = player_mapper
        self._idp: IDProvider = idp

    def execute(self, in_dto: I) -> Player:
        if self._idp and self._idp.get_payer_identity() is not None:
            raise ActionFailed
        player_id = self._player_mapper.add_player(in_dto)
        player = self._player_mapper.get_player(GetPlayerQuery(player_id, None))
        if player is None:
            raise ActionFailed
        self._idm.assign_session(player_id)
        return player
