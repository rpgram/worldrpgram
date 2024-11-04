import dataclasses


@dataclasses.dataclass
class StartBattleHeroDTO:
    health: int
    combo_root_id: int


@dataclasses.dataclass
class StartBattlePlayerDTO:
    name: str
    player_id: int
    hero: StartBattleHeroDTO
