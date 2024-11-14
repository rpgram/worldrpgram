from dataclasses import dataclass
from enum import Enum

from rpgram_setup.domain.user_types import PlayerId, BattleId


class Outcome(int, Enum):
    RUNNING = 0
    WIN = 1
    LEFT = 2
    LOST = 3


@dataclass
class RelatedBattleResult:
    player_id: PlayerId
    is_hero: bool
    outcome: Outcome


@dataclass
class BattleResult:
    battle_id: BattleId
    hero_result: RelatedBattleResult
    opponent_result: RelatedBattleResult
