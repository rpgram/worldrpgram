from rpgram_setup.application.factories import players_hero
from rpgram_setup.domain.exceptions import ActionFailed
from rpgram_setup.domain.factory import HeroFactory
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.vos.in_game import HeroClass
from rpgram_setup.domain.player import Player


def init_hero(hero_factory: HeroFactory, player: Player, hero_class: HeroClass):
    if hero_class == HeroClass.WARRIOR:
        hero = hero_factory.create_warrior()
    elif hero_class == HeroClass.SORCERER:
        hero = hero_factory.create_sorcerer()
    else:
        raise ActionFailed
    player.heroes.append(players_hero(hero))
