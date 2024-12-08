from rpgram_setup.domain.user_types import PlayerId


class BattleKeysGateway:
    def __init__(self) -> None:
        self.db: dict[PlayerId, str] = {}

    def add_key(self, player_id: PlayerId, key: str):
        self.db[player_id] = key

    def get_key(self, player_id: PlayerId) -> str | None:
        return self.db.get(player_id)
