from adaptix import P
from adaptix.conversion import from_param, get_converter, impl_converter, link

from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.infrastructure.models import StartBattleHeroDTO, StartBattlePlayerDTO

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
            P[PlayersHero].born,
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
