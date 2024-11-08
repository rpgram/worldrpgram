from adaptix.conversion import link, impl_converter, coercer, get_converter
from adaptix import P

from rpgram_setup.domain.exceptions import SomethingIsMissing
from rpgram_setup.domain.heroes import PlayersHero, HeroClass
from rpgram_setup.domain.player import Player
from rpgram_setup.infrastructure.models import StartBattlePlayerDTO, StartBattleHeroDTO


def convert_players_hero_to_dto(
    players_hero: PlayersHero,
) -> StartBattleHeroDTO:
    return StartBattleHeroDTO(
        health=players_hero.hero_stats.health,
        combo_root_id=players_hero.hero.class_.value,
    )


def player_to_dto_converter(player: Player, hero: HeroClass) -> StartBattlePlayerDTO:
    try:
        hero = next(h for h in player.heroes if h.hero.class_ == hero)
    except StopIteration:
        raise SomethingIsMissing("hero class")
    return StartBattlePlayerDTO(
        name=player.username,
        player_id=player.player_id,
        hero=convert_players_hero_to_dto(hero),
    )
