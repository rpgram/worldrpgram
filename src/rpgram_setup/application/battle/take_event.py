import logging

from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.core import AsyncInteractor
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper
from rpgram_setup.domain.protocols.data.statisctics import StatisticsWriter


class TakeEventInteractor(AsyncInteractor[BattleResult, None]):
    def __init__(
        self, battle_result_mapper: BattleResultMapper, saver: StatisticsWriter
    ):
        self.long_term_saver = saver
        self.battle_result_mapper = battle_result_mapper

    async def execute(self, in_dto: BattleResult) -> None:
        self.battle_result_mapper.save_result(in_dto)
        await self.long_term_saver.save_battle_result(in_dto)
        logging.warning("Battle has finished.", extra={"scope": "battle"})
