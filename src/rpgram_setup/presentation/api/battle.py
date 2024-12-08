from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from rpgram_setup.application.battle.start_battle import StartBattleDTO
from rpgram_setup.application.battle.wait import WaitingBattleDTOReader
from rpgram_setup.domain.battle import WaitingBattle
from rpgram_setup.domain.exceptions import SomethingIsMissingError
from rpgram_setup.domain.vos.in_game import HeroClass
from rpgram_setup.domain.protocols.core import AsyncInteractor, Interactor
from rpgram_setup.domain.user_types import PlayerId, BattleId
from rpgram_setup.infrastructure.data.gateways import WaitingBattleGateway
from rpgram_setup.infrastructure.exceptions import BadRequest

battle_router = APIRouter(prefix="/battle")


@battle_router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def start_battle(
    player_id: PlayerId,
    opponent_id: PlayerId,
    hero_class: HeroClass,
    interactor: FromDishka[AsyncInteractor[StartBattleDTO, BattleId]],
) -> BattleId:
    start_battle_dto = StartBattleDTO(player_id, opponent_id, hero_class)
    try:
        return await interactor.execute(start_battle_dto)
    except SomethingIsMissingError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Missing: {e}")
    except BadRequest:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Seems broken")


@battle_router.post("/waiters")
@inject
async def start_waiting(
    hero_class: HeroClass, interactor: FromDishka[Interactor[HeroClass, None]]
):
    return interactor.execute(hero_class)


@battle_router.get("/waiters")
@inject
async def get_waiting(
    reader: FromDishka[WaitingBattleDTOReader],
) -> list[WaitingBattle]:
    return reader.get_battles()
