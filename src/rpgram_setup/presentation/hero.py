from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from rpgram_setup.application.hero.init import CreateHeroDTO
from rpgram_setup.application.identity import IDProvider
from rpgram_setup.domain.exceptions import SomethingIsMissing
from rpgram_setup.domain.heroes import HeroClass
from rpgram_setup.domain.protocols.core import AsyncInteractor
from rpgram_setup.domain.user_types import PlayerId
from rpgram_setup.infrastructure.dependencies import id_provider

hero_router = APIRouter(prefix="/hero")


@hero_router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def get_players_hero(
    hero_class: HeroClass,
    interactor: FromDishka[AsyncInteractor[CreateHeroDTO, None]],
    idp: IDProvider = Depends(id_provider),
):
    try:
        await interactor.execute(CreateHeroDTO(idp, hero_class))
    except SomethingIsMissing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Oops")
