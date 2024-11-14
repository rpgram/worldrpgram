from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.core import Interactor, I, O
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper


class TakeEventInteractor(Interactor[BattleResult, None]):
    def __init__(self, battle_result_mapper: BattleResultMapper):
        self.battle_result_mapper = battle_result_mapper

    def execute(self, in_dto: BattleResult) -> None:
        self.battle_result_mapper.save_result(in_dto)
