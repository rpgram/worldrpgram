import abc
import dataclasses
from typing import Any, Protocol

from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.user_types import PlayerId, BattleId


class BattleResultMapper(Protocol):
    db: Any

    @abc.abstractmethod
    def save_result(self, result: BattleResult): ...

    @abc.abstractmethod
    def get_battle_result(self, battle_id: BattleId) -> list[BattleResult]: ...

    @abc.abstractmethod
    def get_results(self, player_id: PlayerId | None = None) -> list[BattleResult]: ...
