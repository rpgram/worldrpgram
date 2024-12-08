import abc
from typing import Any, Protocol

from rpgram_setup.domain.battle import BattleResult, WaitingBattle
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import BattleId, PlayerId


class BattleResultMapper(Protocol):
    db: Any

    @abc.abstractmethod
    def save_result(self, result: BattleResult): ...

    @abc.abstractmethod
    def get_battle_result(self, battle_id: BattleId) -> list[BattleResult]: ...

    @abc.abstractmethod
    def get_results(self, player_id: PlayerId | None = None) -> list[BattleResult]: ...


class UserMapper(Protocol):

    db: Any

    @abc.abstractmethod
    def get_user(self, login: str) -> User | None: ...

    @abc.abstractmethod
    def insert_user(self, user: User): ...


class WaitingBattleGatewayProto(Protocol):

    @abc.abstractmethod
    def insert_battle(self, waiting_battle: WaitingBattle): ...

    @abc.abstractmethod
    def get_battles(self) -> list[WaitingBattle]: ...

    @abc.abstractmethod
    def get_by_player(self, player_id: PlayerId) -> WaitingBattle | None: ...

    @abc.abstractmethod
    def remove_battle(self, player_id: PlayerId): ...
