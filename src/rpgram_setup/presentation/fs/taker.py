from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream import BaseMiddleware
from faststream.rabbit import RabbitRouter

from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.protocols.core import Interactor, AsyncInteractor


def make_rabbit_router(q_dsn: str | None):
    if q_dsn:
        router = RabbitRouter(q_dsn)
    else:
        router = RabbitRouter()

    sub = router.subscriber("events")

    sub(battle_event)
    return router


@inject
async def battle_event(
    event: BattleResult, interactor: FromDishka[AsyncInteractor[BattleResult, None]]
):
    await interactor.execute(event)
