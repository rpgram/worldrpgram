import dataclasses

from rpgram_setup.domain.user_types import PlayerId, BattleId


@dataclasses.dataclass
class StartBattleHeroDTO:
    health: int
    combo_root_id: int


@dataclasses.dataclass
class StartBattlePlayerDTO:
    name: str
    player_id: PlayerId
    hero: StartBattleHeroDTO


@dataclasses.dataclass
class BattleStarted:
    battle_id: BattleId
    player_key: str
    opponent_key: str
