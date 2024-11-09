import dataclasses

from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass
class StartBattleHeroDTO:
    health: int
    combo_root_id: int


@dataclasses.dataclass
class StartBattlePlayerDTO:
    name: str
    player_id: PlayerId
    hero: StartBattleHeroDTO
