from contextlib import suppress

from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.economics import Balance, Token
from rpgram_setup.domain.exceptions import NotUniqueError
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper, UserMapper
from rpgram_setup.domain.protocols.data.players import (
    CreatePlayer,
    GetPlayerQuery,
    GetPlayersQuery,
    PlayersMapper,
)
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import DBS, BattleId, PlayerId


class PlayerMemoryMapper(PlayersMapper):
    db: list[Player]

    def __init__(self, dbs: DBS[type, list[Player]]) -> None:
        self.db = dbs[Player]

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
            raise NotUniqueError("username", create_player.username)
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


class BattleResultMemoryMapper(BattleResultMapper):
    def __init__(self, dbs: DBS[type, list[BattleResult]]) -> None:
        self.db: list[BattleResult] = dbs[BattleResult]

    def save_result(self, result: BattleResult) -> None:
        self.db.append(result)

    def get_results(self, player_id: PlayerId | None = None) -> list[BattleResult]:
        if player_id:
            return [
                br
                for br in self.db
                if player_id in (br.opponent_result.player_id, br.hero_result.player_id)
            ]
        return self.db

    def get_battle_result(self, battle_id: BattleId) -> list[BattleResult]:
        return [br for br in self.db if br.battle_id == battle_id]


class UserMemoryMapper(UserMapper):
    def insert_user(self, user: User) -> None:
        self.db.append(user)

    def __init__(self, dbs: DBS[type, list[User]]) -> None:
        self.db: list[User] = dbs[User]

    def get_user(self, login: str) -> User | None:
        with suppress(StopIteration):
            return next(u for u in self.db if u.login == login)
        return None
