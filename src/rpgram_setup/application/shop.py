import dataclasses

from rpgram_setup.domain.entities import Shop
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.user_types import MinMax, MinMaxMoney
from rpgram_setup.domain.vos.in_game import Good, HeroClass


@dataclasses.dataclass
class ShopSearch:
    level: MinMax
    price: MinMaxMoney
    hero: HeroClass | None = None
    name_part: str | None = None


class SearchOffer(Interactor[ShopSearch, list[Good]]):
    def __init__(self, shop: Shop):
        self.shop = shop

    def execute(self, in_dto: ShopSearch) -> list[Good]:
        return self.shop.search(
            in_dto.level, in_dto.price, in_dto.name_part, in_dto.hero
        )
