from adaptix.conversion import (
    get_converter,
    link,
    impl_converter,
    from_param,
    link_function,
)
from adaptix import P

from rpgram_setup.domain.heroes import Hero, PlayersHero


# @impl_converter(recipe=[
#     link(P[Hero].default_stats, P[PlayersHero].hero_stats),
#     link(P[Hero].equipment, P[PlayersHero].item),
#     link(from_param("copied"), P[PlayersHero].hero)
# ])
players_hero = get_converter(
    Hero,
    PlayersHero,
    recipe=[
        link(P[Hero].default_stats, P[PlayersHero].hero_stats),
        link(P[Hero].equipment, P[PlayersHero].item),
        link_function(lambda h: h, P[PlayersHero].hero),
    ],
)
