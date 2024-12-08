import dataclasses

from rpgram_setup.application.identity import IDProvider
from rpgram_setup.domain.consts import HERO_MAX_LVL, MAX_ITEM_PRICE
from rpgram_setup.domain.economics import Token
from rpgram_setup.domain.entities import Shop
from rpgram_setup.domain.exceptions import (
    ActionFailedError,
    SomethingIsMissingError,
    NotUniqueError,
)
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor, I, O, AsyncInteractor
from rpgram_setup.domain.protocols.data.players import PlayersMapper, GetPlayerQuery
from rpgram_setup.domain.protocols.data.statisctics import StatisticsWriter, TradeEvent
from rpgram_setup.domain.vos.in_game import Equipment


class EquipInteractor(Interactor[int, PlayersHero]):
    def __init__(self, idp: IDProvider, players: PlayersMapper):
        self.idp = idp
        self.players = players

    def execute(self, in_dto: int) -> PlayersHero:
        self.idp.authenticated_only()
        player = self.players.get_player(
            GetPlayerQuery(self.idp.get_payer_identity(), None)
        )
        if player is None:
            raise ActionFailedError
        for slot in player.inventory:
            if slot.slot_id == in_dto:
                if not isinstance(slot.item, Equipment):
                    raise ActionFailedError
                break
        else:
            raise SomethingIsMissingError("slot")
        for hero in player.heroes:
            if hero.born.class_ == slot.item.class_:
                hero.equip(slot.item)
                return hero
        raise SomethingIsMissingError("hero")


@dataclasses.dataclass
class BuyCommand:
    name: str
    quantity: int


class BuyInteractor(AsyncInteractor[BuyCommand, Player]):
    def __init__(
        self,
        shop: Shop,
        players: PlayersMapper,
        idp: IDProvider,
        stats_writer: StatisticsWriter,
    ):
        self.stats_writer = stats_writer
        self.idp = idp
        self.shop = shop
        self.players = players

    async def execute(self, in_dto: BuyCommand) -> Player:
        self.idp.authenticated_only()
        items = self.shop.search(
            (0, HERO_MAX_LVL), (Token(0), Token(MAX_ITEM_PRICE)), in_dto.name, None
        )
        if len(items) != 1:
            raise NotUniqueError("item", in_dto)
        player = self.players.get_player(
            GetPlayerQuery(self.idp.get_payer_identity(), None)
        )
        if player is None:
            raise ActionFailedError
        player.buy(items[0], in_dto.quantity)
        trade_event = TradeEvent(
            True, items[0], in_dto.quantity, self.shop.get(items[0], in_dto.quantity)
        )
        await self.stats_writer.trade(trade_event)
        return player
