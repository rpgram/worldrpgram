from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from rpgram_setup.application.equipment import BuyCommand
from rpgram_setup.application.shop import ShopSearch
from rpgram_setup.domain.consts import HERO_MAX_LVL, MAX_ITEM_PRICE
from rpgram_setup.domain.economics import Money
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor, AsyncInteractor
from rpgram_setup.domain.vos.in_game import Good, HeroClass
from rpgram_setup.presentation.converters import (
    good_to_good_dto,
    players_to_hero_dto,
    convert_player_to_dto,
)
from rpgram_setup.presentation.models import GoodDTO, PlayerDTO, HeroDTO

equip_router = APIRouter(prefix="/equipment")


@equip_router.get("/shops")
@inject
async def get_shop_goods(
    interactor: FromDishka[Interactor[ShopSearch, list[Good]]],
    min_lvl: int = 0,
    max_lvl: int = HERO_MAX_LVL,
    min_tokens: int = 0,
    max_tokens: int = MAX_ITEM_PRICE,
    hero_class: HeroClass | None = None,
    name_part: str | None = None,
) -> list[GoodDTO]:
    return [
        good_to_good_dto(g)
        for g in interactor.execute(
            ShopSearch(
                (min_lvl, max_lvl),
                (Money(min_tokens), Money(max_tokens)),
                hero_class,
                name_part,
            )
        )
    ]


@equip_router.post("/buy")
@inject
async def buy_item(
    buy: BuyCommand, interactor: FromDishka[AsyncInteractor[BuyCommand, Player]]
) -> PlayerDTO:
    return convert_player_to_dto(await interactor.execute(buy))


@equip_router.post("/wear")
@inject
async def wear_item(
    slot_id: int, interactor: FromDishka[Interactor[int, PlayersHero]]
) -> HeroDTO:
    return players_to_hero_dto(interactor.execute(slot_id))
