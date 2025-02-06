from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from rpgram_setup.application.hero.init import CreateHeroDTO
from rpgram_setup.domain.exceptions import SomethingIsMissingError
from rpgram_setup.domain.protocols.core import AsyncInteractor
from rpgram_setup.domain.vos.in_game import HeroClass

hero_router = APIRouter(prefix="/hero")


@hero_router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def get_players_hero(
    hero_class: HeroClass,
    interactor: FromDishka[AsyncInteractor[CreateHeroDTO, None]],
) -> None:
    try:
        await interactor.execute(CreateHeroDTO(hero_class))
    except SomethingIsMissingError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Oops")
