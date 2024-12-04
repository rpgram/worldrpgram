from dishka import AsyncContainer

from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.players import PlayersMapper, GetPlayersQuery


class GiveawayInteractor(Interactor[None, None]):
    def __init__(
        self, players_mapper: PlayersMapper, request_container: AsyncContainer
    ):
        self.request_container = request_container
        self.players_mapper = players_mapper

    def execute(self, in_dto: None) -> None:
        players = self.players_mapper.get_players(GetPlayersQuery(0, 0))
        ...
        # for player in players:
        # for player in players:
        #     async with self.request_container(context={Player: player}) as action:
        #         transactor = await action.get()
