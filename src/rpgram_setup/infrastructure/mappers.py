from contextlib import suppress

from rpgram_setup.domain.economics import Balance, Token
from rpgram_setup.domain.exceptions import NotUnique
from rpgram_setup.domain.factory import HeroFactory
from rpgram_setup.domain.heroes import HeroClass, PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.data.players import (
    PlayersMapper,
    GetPlayerQuery,
    CreatePlayer,
    GetPlayersQuery,
)
from rpgram_setup.domain.user_types import PlayerId, DB


class PlayerMemoryMapper(PlayersMapper):

    db: list[Player]

    def __init__(self, db: DB):
        self.db = db

    def _apply_get_player(self, query: GetPlayerQuery, player: Player) -> bool:
        by_id = query.player_id and query.player_id == player.player_id
        if by_id:
            return True
        return bool(query.username and query.username == player.username)

    def get_player(self, query: GetPlayerQuery) -> Player | None:
        assert query.player_id or query.username
        with suppress(StopIteration):
            return next(p for p in self.db if self._apply_get_player(query, p))
        return None

    def get_players(self, query: GetPlayersQuery) -> list[Player]:
        end_pointer = query.skip + query.limit if query.limit else None
        return self.db[query.skip : end_pointer]

    def _generate_id(self) -> PlayerId:
        return PlayerId(len(self.db) + 1)

    def add_player(self, create_player: CreatePlayer) -> PlayerId:
        exists = self.get_player(GetPlayerQuery(None, create_player.username))
        if exists is not None:
            raise NotUnique("username", create_player.username)
        player_id = self._generate_id()
        player = Player(
            balance=Balance({Token: Token(150)}),
            inventory=[],
            heroes=[],
            username=create_player.username,
            player_id=player_id,
        )
        self.db.append(player)
        return player_id
