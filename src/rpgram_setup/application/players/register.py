from rpgram_setup.application.identity import (
    SessionIDManager,
    RSessionIDManager,
    IDProvider,
)
from rpgram_setup.domain.player import Player
from rpgram_setup.presentation.converters import convert_player_to_dto
from rpgram_setup.presentation.models import PlayerDTO
from rpgram_setup.domain.exceptions import ActionFailed, WorldException
from rpgram_setup.domain.protocols.core import Interactor, I
from rpgram_setup.domain.protocols.data.players import (
    CreatePlayer,
    PlayersMapper,
    GetPlayerQuery,
)


class NewPlayerInteractor(Interactor[CreatePlayer, Player]):
    def __init__(self, player_mapper: PlayersMapper, idm: RSessionIDManager):
        self._idm = idm
        self._player_mapper = player_mapper
        self._idp: IDProvider | None = None

    def set_id_provider(self, id_provider: IDProvider):
        self._idp = id_provider

    def execute(self, in_dto: I) -> Player:
        if self._idp and self._idp.get_payer_identity():
            raise ActionFailed
        player_id = self._player_mapper.add_player(in_dto)
        player = self._player_mapper.get_player(GetPlayerQuery(player_id, None))
        if player is None:
            raise ActionFailed
        self._idm.login(player_id)
        return player
