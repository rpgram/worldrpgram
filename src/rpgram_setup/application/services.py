from rpgram_setup.application.factories import players_hero
from rpgram_setup.domain.factory import HeroFactory
from rpgram_setup.domain.heroes import HeroClass, PlayersHero
from rpgram_setup.domain.player import Player


def init_hero(hero_factory: HeroFactory, player: Player, hero_class: HeroClass):
    if hero_class == HeroClass.WARRIOR:
        player.heroes.append(players_hero(hero_factory.create_warrior()))
