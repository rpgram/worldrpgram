import dataclasses

from rpgram_setup.domain.exceptions import LevelTooLow, BattleContinues
from rpgram_setup.domain.vos.in_game import Hero, HeroStats, Equipment


@dataclasses.dataclass
class PlayersHero:
    """Holds characteristics related to hero class. Can level up."""

    born: Hero
    hero_stats: HeroStats
    item: Equipment | None
    locked = False
    level = 1
    # def __init__(self, hero: Hero):
    #     self.hero = hero
    #     self.hero_stats = hero.default_stats
    #     self.item: Equipment | None = hero.equipment
    #     self.locked = False
    #     self.level = 1

    def _wear(self, item: Equipment) -> None:
        """Only items with same class are displayed."""
        if self.level < item.required_level:
            raise LevelTooLow
        self.hero_stats.armor += item.stats_diff.armor
        self.hero_stats.damage += item.stats_diff.damage
        self.hero_stats.health += item.stats_diff.health
        self.item = item

    def take_off(self) -> None:
        if self.locked:
            raise BattleContinues
        if self.item is None:
            return
        self.hero_stats.armor -= self.item.stats_diff.armor
        self.hero_stats.damage -= self.item.stats_diff.damage
        self.hero_stats.health -= self.item.stats_diff.health
        self.item = None

    def equip(self, item: Equipment) -> None:
        self.take_off()
        self._wear(item)

    def level_up(self):
        self.born.level_up(self.hero_stats)
