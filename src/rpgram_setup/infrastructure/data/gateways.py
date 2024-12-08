from contextlib import suppress
from typing import Mapping

from rpgram_setup.application.battle.wait import WaitingBattleDTOReader
from rpgram_setup.domain.battle import WaitingBattle
from rpgram_setup.domain.protocols.data.battle import WaitingBattleGatewayProto
from rpgram_setup.domain.user_types import DBS, PlayerId


class BattleKeysGateway:
    def __init__(self) -> None:
        self.db: dict[PlayerId, str] = {}

    def add_key(self, player_id: PlayerId, key: str):
        self.db[player_id] = key

    def get_key(self, player_id: PlayerId) -> str | None:
        return self.db.get(player_id)


class WaitingBattleGateway(WaitingBattleGatewayProto, WaitingBattleDTOReader):
    def __init__(self, db: DBS):
        self.db: list[WaitingBattle] = db[WaitingBattle]

    def insert_battle(self, battle: WaitingBattle):
        self.db.append(battle)

    def get_battles(self) -> list[WaitingBattle]:
        return self.db

    def get_by_player(self, player_id: PlayerId) -> WaitingBattle | None:
        with suppress(StopIteration):
            return next(wb for wb in self.db if wb.player_id == player_id)
        return None

    def remove_battle(self, player_id: PlayerId):
        self.db = [wb for wb in self.db if wb.player_id != player_id]
