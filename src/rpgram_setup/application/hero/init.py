import dataclasses

from rpgram_setup.application.identity import IDProvider
from rpgram_setup.application.services import init_hero
from rpgram_setup.domain.exceptions import NotUniqueError, SomethingIsMissingError
from rpgram_setup.domain.factory import HeroFactory
from rpgram_setup.domain.protocols.core import AsyncInteractor
from rpgram_setup.domain.protocols.data.players import GetPlayerQuery, PlayersMapper
from rpgram_setup.domain.vos.in_game import HeroClass


@dataclasses.dataclass
class CreateHeroDTO:
    hero_class: HeroClass


class InitHeroInteractor(AsyncInteractor[CreateHeroDTO, None]):

    def __init__(
        self, player_mapper: PlayersMapper, hero_factory: HeroFactory, idp: IDProvider
    ):
        self.idp = idp
        self.hero_factory = hero_factory
        self.player_mapper = player_mapper

    async def execute(self, in_dto: CreateHeroDTO) -> None:
        self.idp.authenticated_only()
        player = self.player_mapper.get_player(
            GetPlayerQuery(self.idp.get_payer_identity(), None)
        )
        if player is None:
            raise SomethingIsMissingError("player")
        for hero in player.heroes:
            if hero.born.class_ == in_dto.hero_class:
                raise NotUniqueError("hero", in_dto.hero_class)
        init_hero(self.hero_factory, player, in_dto.hero_class)
