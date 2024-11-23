from adaptix.conversion import link, impl_converter, coercer, get_converter, from_param
from adaptix import P

from rpgram_setup.domain.exceptions import SomethingIsMissing
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.vos.in_game import Hero, HeroStats, HeroClass
from rpgram_setup.domain.player import Player
from rpgram_setup.infrastructure.models import StartBattlePlayerDTO, StartBattleHeroDTO


convert_players_hero_to_dto = get_converter(
    PlayersHero,
    StartBattleHeroDTO,
    recipe=[
        link(
            P[PlayersHero].hero_stats,
            P[StartBattleHeroDTO].health,
            coercer=lambda hs: hs.health,
        ),
        link(
            P[PlayersHero].hero,
            P[StartBattleHeroDTO].combo_root_id,
            coercer=lambda hero: hero.class_,
        ),
    ],
)


@impl_converter(
    recipe=[
        link(
            from_param("hero"),
            P[StartBattlePlayerDTO].hero,
            coercer=convert_players_hero_to_dto,
        ),
        link(P[Player].username, P[StartBattlePlayerDTO].name),
    ]
)
def player_to_dto_converter(  # type: ignore[empty-body]
    player: Player, hero: PlayersHero
) -> StartBattlePlayerDTO: ...
