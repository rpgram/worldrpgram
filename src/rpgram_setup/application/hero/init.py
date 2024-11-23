import dataclasses

from rpgram_setup.application.identity import IDProvider
from rpgram_setup.application.services import init_hero
from rpgram_setup.domain.exceptions import SomethingIsMissing
from rpgram_setup.domain.factory import HeroFactory
from rpgram_setup.domain.vos.in_game import HeroClass
from rpgram_setup.domain.protocols.core import AsyncInteractor, I, O
from rpgram_setup.domain.protocols.data.players import PlayersMapper, GetPlayerQuery


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
            raise SomethingIsMissing("player")
        init_hero(self.hero_factory, player, in_dto.hero_class)
