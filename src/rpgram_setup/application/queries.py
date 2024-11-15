import dataclasses

from rpgram_setup.domain.user_types import PlayerId, BattleId


@dataclasses.dataclass
class BattleResultsQuery:
    player_id: PlayerId | None = None
    battle_id: BattleId | None = None