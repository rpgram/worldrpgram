from adaptix.conversion import (
    get_converter,
    link,
    link_function,
)
from adaptix import P

from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.vos.in_game import Hero

players_hero = get_converter(
    Hero,
    PlayersHero,
    recipe=[
        link(P[Hero].default_stats, P[PlayersHero].hero_stats),
        link(P[Hero].equipment, P[PlayersHero].item),
        link_function(lambda h: h, P[PlayersHero].hero),
    ],
)
