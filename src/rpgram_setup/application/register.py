from rpgram_setup.application.converters import convert_player_to_dto
from rpgram_setup.application.models import PlayerDTO
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor, I, O
from rpgram_setup.domain.protocols.data.players import (
    CreatePlayer,
    PlayersMapper,
    GetPlayerQuery,
)


class NewPlayerInteractor(Interactor[CreatePlayer, PlayerDTO]):
    def __init__(self, player_mapper: PlayersMapper):
        self._player_mapper = player_mapper

    def execute(self, in_dto: I) -> PlayerDTO:
        player_id = self._player_mapper.add_player(in_dto)
        player = self._player_mapper.get_player(GetPlayerQuery(player_id, None))
        return convert_player_to_dto(player)
