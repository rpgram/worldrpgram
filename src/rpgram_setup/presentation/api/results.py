from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from rpgram_setup.application.queries import BattleResultsQuery
from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper
from rpgram_setup.domain.user_types import PlayerId, BattleId

results_router = APIRouter(prefix="/results")


@results_router.get("")
@inject
async def get_results(
    interactor: FromDishka[Interactor[BattleResultsQuery, list[BattleResult]]],
    player_id: PlayerId | None = None,
    battle_id: BattleId | None = None,
) -> list[BattleResult]:
    return interactor.execute(BattleResultsQuery(player_id, battle_id))
