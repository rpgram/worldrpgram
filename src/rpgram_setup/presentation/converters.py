from adaptix.conversion import coercer
from adaptix.conversion import get_converter

from rpgram_setup.presentation.models import PlayerDTO, GoodDTO
from rpgram_setup.domain.economics import Balance
from rpgram_setup.domain.heroes import PlayersHero, HeroClass
from rpgram_setup.domain.items import Good
from rpgram_setup.domain.player import Player


def good_to_good_dto(good: Good) -> GoodDTO:
    return GoodDTO(price=[str(good.price)], quantity=good.quantity, name=good.name)


convert_player_to_dto = get_converter(
    Player,
    PlayerDTO,
    recipe=[
        coercer(Balance, str, str),
        coercer(
            list[Good], list[GoodDTO], lambda gl: [good_to_good_dto(i) for i in gl]
        ),
        coercer(
            list[PlayersHero],
            list[HeroClass],
            lambda lph: [ph.hero.class_ for ph in lph],
        ),
    ],
)
