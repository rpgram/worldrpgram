from adaptix.conversion import coercer, get_converter

from rpgram_setup.domain.economics import Balance
from rpgram_setup.domain.entities import Slot
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.vos.in_game import Good, HeroClass
from rpgram_setup.presentation.models import GoodDTO, HeroDTO, PlayerDTO, SlotDTO


def players_to_hero_dto(ph: PlayersHero) -> HeroDTO:
    return HeroDTO(
        level=ph.level,
        health=ph.hero_stats.health,
        hero_class=ph.born.class_,
        equipment=None if ph.item is None else ph.item.name,
    )


def good_to_good_dto(good: Good) -> GoodDTO:
    return GoodDTO(price=[str(good.price_per_unit)], name=good.name)


slot_converter = get_converter(
    Slot, SlotDTO, recipe=[coercer(Good, GoodDTO, good_to_good_dto)]
)


convert_player_to_dto = get_converter(
    Player,
    PlayerDTO,
    recipe=[
        coercer(Balance, str, str),
        coercer(list[Slot], list[SlotDTO], lambda sl: [slot_converter(i) for i in sl]),
        coercer(
            list[PlayersHero],
            list[HeroClass],
            lambda lph: [ph.born.class_ for ph in lph],
        ),
    ],
)
