from rpgram_setup.domain.heroes import Hero, HeroStats, HeroClass


class HeroFactory:

    def create_warrior(self) -> Hero:
        hero_stats = HeroStats(100, 13, 25)
        per_level = HeroStats(10, 1, 2)
        return Hero(hero_stats, per_level, HeroClass.WARRIOR, None)
