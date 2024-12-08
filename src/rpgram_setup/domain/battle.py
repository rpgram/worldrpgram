import dataclasses
from dataclasses import dataclass
from enum import Enum

from rpgram_setup.domain.user_types import PlayerId, BattleId
from rpgram_setup.domain.vos.in_game import HeroClass


class Outcome(int, Enum):
    RUNNING = 0
    WIN = 1
    LEFT = 2
    LOST = 3


@dataclass
class RelatedBattleResult:
    player_id: PlayerId
    is_hero: bool
    win: bool
    # outcome: Outcome


@dataclass
class BattleResult:
    battle_id: BattleId
    hero_result: RelatedBattleResult
    opponent_result: RelatedBattleResult


@dataclasses.dataclass
class WaitingBattle:
    player_id: PlayerId
    hero_class: HeroClass
