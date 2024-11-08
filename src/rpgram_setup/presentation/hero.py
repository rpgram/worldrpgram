from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from rpgram_setup.application.hero.init import CreateHeroDTO
from rpgram_setup.domain.exceptions import SomethingIsMissing
from rpgram_setup.domain.heroes import HeroClass
from rpgram_setup.domain.protocols.core import AsyncInteractor
from rpgram_setup.domain.user_types import PlayerId

hero_router = APIRouter(prefix="/hero")


@hero_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def get_players_hero(
    player_id: PlayerId,
    hero_class: HeroClass,
    interactor: FromDishka[AsyncInteractor[CreateHeroDTO, None]],
):
    try:
        await interactor.execute(CreateHeroDTO(player_id, hero_class))
    except SomethingIsMissing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Oops")
