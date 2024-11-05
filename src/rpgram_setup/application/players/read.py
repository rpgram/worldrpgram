from rpgram_setup.domain.exceptions import ActionFailed
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor, I, O
from rpgram_setup.domain.protocols.data.players import PlayersMapper, GetPlayersQuery, GetPlayerQuery


class ReadPlayersInteractor(Interactor[GetPlayersQuery, list[Player]]):
    def __init__(self, player_data_mapper: PlayersMapper):
        self.mapper = player_data_mapper

    def execute(self, in_dto: GetPlayersQuery) -> list[Player]:
        return self.mapper.get_players(in_dto)


class ReadPlayerInteractor(Interactor[GetPlayerQuery, Player]):
    def __init__(self, player_data_mapper: PlayersMapper):
        self.mapper = player_data_mapper

    def execute(self, in_dto: GetPlayerQuery) -> Player:
        player = self.mapper.get_player(in_dto)
        if player is None:
            raise ActionFailed
        return player
