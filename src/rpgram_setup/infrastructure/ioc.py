import collections
from typing import Iterable, Iterator, AsyncIterable

from asynch import connect
from dishka import (
    Scope,
    provide,
    make_async_container,
    AsyncContainer,
    from_context,
    AnyOf,
)
from dishka.integrations.fastapi import FastapiProvider
from starlette.requests import Request

from rpgram_setup.application.auth import (
    UserLoginDTO,
    UserLoginInteractor,
    UserRegisterDTO,
    UserRegisterInteractor,
    GetKeyInteractor,
)
from rpgram_setup.application.battle.results import BattleResultsInteractor
from rpgram_setup.application.equipment import (
    EquipInteractor,
    BuyCommand,
    BuyInteractor,
)
from rpgram_setup.application.identity import (
    RSessionIDManager,
    SessionDB,
    IDProvider,
)
from rpgram_setup.application.queries import BattleResultsQuery
from rpgram_setup.application.battle.take_event import TakeEventInteractor
from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.application.hero.init import InitHeroInteractor, CreateHeroDTO
from rpgram_setup.application.players.read import (
    ReadPlayersInteractor,
    ReadPlayerInteractor,
)
from rpgram_setup.application.players.create_profile import NewPlayerInteractor
from rpgram_setup.application.battle.start_battle import (
    StartBattleInteractor,
    StartBattleDTO,
)
from rpgram_setup.application.shop import SearchOffer, ShopSearch
from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.entities import Shop
from rpgram_setup.domain.factory import (
    HeroFactory,
    NullSuiteFactory,
    CentralShopFactory,
)
from rpgram_setup.domain.gateways import RequestData
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import (
    ClientProto,
    ConnectorProto,
    AsyncInteractor,
    Interactor,
)
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper, UserMapper
from rpgram_setup.domain.protocols.data.players import (
    PlayersMapper,
    CreatePlayer,
    GetPlayersQuery,
    GetPlayerQuery,
)
from rpgram_setup.domain.protocols.data.statisctics import StatisticsWriter
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import BattleId, DBS
from rpgram_setup.domain.vos.in_game import Good
from rpgram_setup.infrastructure.api import SessionManager, BattleAPIClient
from rpgram_setup.infrastructure.config import read_config
from rpgram_setup.infrastructure.data.clickhouse_stats import ClickHouseWriter
from rpgram_setup.infrastructure.data.gateways import BattleKeysGateway
from rpgram_setup.infrastructure.general import HasherImpl
from rpgram_setup.infrastructure.data.mappers import (
    PlayerMemoryMapper,
    BattleResultMemoryMapper,
    UserMemoryMapper,
)
from rpgram_setup.infrastructure.session import RSessionIDManagerImpl, IDProviderImpl


class IoC(FastapiProvider):

    session = provide(
        source=SessionManager,
        provides=ConnectorProto[RequestData[BattleId], BattleId],
        scope=Scope.APP,
    )

    init_hero = provide(
        InitHeroInteractor, provides=AsyncInteractor[CreateHeroDTO, None]
    )

    save_result = provide(
        TakeEventInteractor, provides=AsyncInteractor[BattleResult, None]
    )

    results_mapper = provide(BattleResultMemoryMapper, provides=BattleResultMapper)

    auth_db = from_context(SessionDB, scope=Scope.APP)

    id_manager = provide(RSessionIDManagerImpl, provides=RSessionIDManager)

    hasher = provide(HasherImpl, provides=Hasher, scope=Scope.APP)

    user_login = provide(UserLoginInteractor, provides=Interactor[UserLoginDTO, User])

    user_registration = provide(
        UserRegisterInteractor, provides=Interactor[UserRegisterDTO, User]
    )

    get_results = provide(
        BattleResultsInteractor,
        provides=Interactor[BattleResultsQuery, list[BattleResult]],
    )

    @provide(scope=Scope.APP)
    def db(self) -> DBS:
        return collections.defaultdict(list)

    user_mapper = provide(UserMemoryMapper, provides=UserMapper)

    hero_factory = provide(HeroFactory)

    battle_connector = provide(
        source=BattleAPIClient, provides=ClientProto, scope=Scope.APP
    )

    keys_gateway = provide(BattleKeysGateway)

    get_key_interactor = provide(GetKeyInteractor)

    scope = Scope.REQUEST

    config = from_context(AppConfig, scope=Scope.APP)

    player_mapper = provide(
        source=PlayerMemoryMapper, provides=PlayersMapper, scope=Scope.APP
    )
    start_battle_interactor = provide(
        StartBattleInteractor, provides=AsyncInteractor[StartBattleDTO, BattleId]
    )
    register_interactor = provide(
        NewPlayerInteractor,
        provides=AnyOf[Interactor[CreatePlayer, Player], NewPlayerInteractor],
    )
    get_all_interactor = provide(
        ReadPlayersInteractor, provides=Interactor[GetPlayersQuery, list[Player]]
    )
    get_interactor = provide(
        ReadPlayerInteractor, provides=Interactor[GetPlayerQuery, Player]
    )

    equip_interactor = provide(EquipInteractor, provides=Interactor[int, PlayersHero])

    shop_offer_interactor = provide(
        SearchOffer, provides=Interactor[ShopSearch, list[Good]]
    )
    buy_interactor = provide(
        BuyInteractor, provides=AsyncInteractor[BuyCommand, Player]
    )

    items_factory = provide(NullSuiteFactory, scope=Scope.APP)
    central_factory = provide(CentralShopFactory, scope=Scope.APP)

    @provide
    async def stats_writer(self, config: AppConfig) -> AsyncIterable[StatisticsWriter]:
        con = await connect(config.ch_dsn)
        async with con.cursor() as cursor:
            yield ClickHouseWriter(cursor)
        await con.close()

    @provide(scope=Scope.APP)
    def shop(self, shop_fac: CentralShopFactory) -> Shop:
        return shop_fac.create_shop()

    @provide
    def auth_provider(self, db: SessionDB, request: Request) -> IDProvider:
        rsession_id = request.cookies.get("RSESSION_ID")
        return IDProviderImpl(rsession_id, db)


def make_container(session_db: SessionDB) -> AsyncContainer:
    config = read_config()
    return make_async_container(
        IoC(), context={AppConfig: config, SessionDB: session_db}
    )
