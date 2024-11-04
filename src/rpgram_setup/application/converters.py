from adaptix.conversion import link, coercer
from adaptix.conversion import get_converter
from adaptix import P

from rpgram_setup.application.models import PlayerDTO, GoodDTO
from rpgram_setup.domain.economics import Balance, Token
from rpgram_setup.domain.heroes import PlayersHero, HeroClass
from rpgram_setup.domain.items import Good
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.user_types import PlayerId


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
