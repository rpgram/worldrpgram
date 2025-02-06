import collections
from typing import AsyncIterable, Any

from asynch import connect
from dishka import (
    AnyOf,
    AsyncContainer,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import FastapiProvider
from starlette.requests import Request

from rpgram_setup.application.auth import (
    GetKeyInteractor,
    UserLoginDTO,
    UserLoginInteractor,
    UserRegisterDTO,
    UserRegisterInteractor,
)
from rpgram_setup.application.battle.results import BattleResultsInteractor
from rpgram_setup.application.battle.start_battle import (
    StartBattleDTO,
    StartBattleInteractor,
)
from rpgram_setup.application.battle.take_event import TakeEventInteractor
from rpgram_setup.application.battle.wait import (
    WaitForOpponentInteractor,
    WaitingBattleDTOReader,
)
from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.application.equipment import (
    BuyCommand,
    BuyInteractor,
    EquipInteractor,
)
from rpgram_setup.application.hero.init import CreateHeroDTO, InitHeroInteractor
from rpgram_setup.application.identity import IDProvider, SessionDB, SessionManager
from rpgram_setup.application.players.create_profile import NewPlayerInteractor
from rpgram_setup.application.players.read import (
    ReadPlayerInteractor,
    ReadPlayersInteractor,
)
from rpgram_setup.application.queries import BattleResultsQuery
from rpgram_setup.application.shop import SearchOffer, ShopSearch
from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.entities import Shop
from rpgram_setup.domain.factory import (
    CentralShopFactory,
    HeroFactory,
    NullSuiteFactory,
)
from rpgram_setup.domain.gateways import RequestData
from rpgram_setup.domain.heroes import PlayersHero
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import (
    AsyncInteractor,
    ClientProto,
    ConnectorProto,
    Interactor,
)
from rpgram_setup.domain.protocols.data.battle import (
    BattleResultMapper,
    UserMapper,
    WaitingBattleGatewayProto,
)
from rpgram_setup.domain.protocols.data.players import (
    CreatePlayer,
    GetPlayerQuery,
    GetPlayersQuery,
    PlayersMapper,
)
from rpgram_setup.domain.protocols.data.statisctics import (
    StatisticsWriter,
    AnalyticsBatcher,
)
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import DBS, BattleId
from rpgram_setup.domain.vos.in_game import Good, HeroClass
from rpgram_setup.infrastructure.api import BattleAPIClient, HTTPSessionManager
from rpgram_setup.infrastructure.config import read_config
from rpgram_setup.infrastructure.consts import SESSION_NAME
from rpgram_setup.infrastructure.data.clickhouse.stats import (
    AnalyticsWriteRepository,
    ClickHouseBatcher,
)
from rpgram_setup.infrastructure.data.gateways import (
    BattleKeysGateway,
    WaitingBattleGateway,
)
from rpgram_setup.infrastructure.data.mappers import (
    BattleResultMemoryMapper,
    PlayerMemoryMapper,
    UserMemoryMapper,
)
from rpgram_setup.infrastructure.general import HasherImpl
from rpgram_setup.infrastructure.models import BattleStarted
from rpgram_setup.infrastructure.session import IDProviderImpl, SessionManagerImpl


class IoC(FastapiProvider):
    session = provide(
        source=HTTPSessionManager,
        provides=ConnectorProto[RequestData[BattleStarted], BattleStarted],
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

    id_manager = provide(SessionManagerImpl, provides=SessionManager)

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
    def db(self) -> DBS[Any, list[Any]]:
        return collections.defaultdict(list)

    user_mapper = provide(UserMemoryMapper, provides=UserMapper)

    hero_factory = provide(HeroFactory)

    battle_connector = provide(
        source=BattleAPIClient, provides=ClientProto, scope=Scope.APP
    )

    keys_gateway = provide(BattleKeysGateway, scope=Scope.APP)

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
    waiting_create = provide(
        WaitForOpponentInteractor, provides=Interactor[HeroClass, None]
    )

    waiters = provide(
        WaitingBattleGateway,
        provides=AnyOf[WaitingBattleDTOReader, WaitingBattleGatewayProto],
    )

    @provide(scope=Scope.APP)
    async def stats_batcher(self, config: AppConfig) -> AsyncIterable[AnalyticsBatcher]:
        con = await connect(config.ch_dsn)
        yield ClickHouseBatcher(con)
        await con.close()

    @provide
    async def stats_writer(self, batcher: AnalyticsBatcher) -> StatisticsWriter:
        return AnalyticsWriteRepository(batcher)

    @provide(scope=Scope.APP)
    def shop(self, shop_fac: CentralShopFactory) -> Shop:
        return shop_fac.create_shop()

    @provide
    def auth_provider(self, db: SessionDB, request: Request) -> IDProvider:
        rsession_id = request.cookies.get(SESSION_NAME)
        return IDProviderImpl(rsession_id, db)


def make_container(session_db: SessionDB) -> AsyncContainer:
    config = read_config()
    return make_async_container(
        IoC(), context={AppConfig: config, SessionDB: session_db}
    )
