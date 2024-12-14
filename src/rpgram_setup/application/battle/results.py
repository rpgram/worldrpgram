from rpgram_setup.application.queries import BattleResultsQuery
from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper


class BattleResultsInteractor(Interactor[BattleResultsQuery, list[BattleResult]]):
    def __init__(self, results_mapper: BattleResultMapper):
        self.results_mapper = results_mapper

    def execute(self, in_dto: BattleResultsQuery) -> list[BattleResult]:
        if in_dto.battle_id:
            return self.results_mapper.get_battle_result(in_dto.battle_id)
        return self.results_mapper.get_results(in_dto.player_id)
