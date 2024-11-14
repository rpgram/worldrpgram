import collections

from dishka import (
    Provider,
    Scope,
    provide,
    make_async_container,
    AsyncContainer,
    from_context,
)

from rpgram_setup.application.battle.results import BattleResultsInteractor
from rpgram_setup.application.queries import BattleResultsQuery
from rpgram_setup.application.battle.take_event import TakeEventInteractor
from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.application.hero.init import InitHeroInteractor, CreateHeroDTO
from rpgram_setup.application.players.read import (
    ReadPlayersInteractor,
    ReadPlayerInteractor,
)
from rpgram_setup.application.players.register import NewPlayerInteractor
from rpgram_setup.application.battle.start_battle import (
    StartBattleInteractor,
    StartBattleDTO,
)
from rpgram_setup.domain.battle import BattleResult
from rpgram_setup.domain.factory import HeroFactory
from rpgram_setup.domain.gateways import RequestData
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import (
    ClientProto,
    ConnectorProto,
    AsyncInteractor,
    Interactor,
)
from rpgram_setup.domain.protocols.data.battle import BattleResultMapper
from rpgram_setup.domain.protocols.data.players import (
    PlayersMapper,
    CreatePlayer,
    GetPlayersQuery,
    GetPlayerQuery,
)
from rpgram_setup.domain.user_types import BattleId, DBS
from rpgram_setup.infrastructure.api import SessionManager, BattleAPIClient
from rpgram_setup.infrastructure.config import read_config
from rpgram_setup.infrastructure.mappers import (
    PlayerMemoryMapper,
    BattleResultMemoryMapper,
)


class IoC(Provider):

    session = provide(
        source=SessionManager,
        provides=ConnectorProto[RequestData[BattleId], BattleId],
        scope=Scope.APP,
    )

    init_hero = provide(
        InitHeroInteractor, provides=AsyncInteractor[CreateHeroDTO, None]
    )

    save_result = provide(TakeEventInteractor, provides=Interactor[BattleResult, None])

    results_mapper = provide(BattleResultMemoryMapper, provides=BattleResultMapper)

    get_results = provide(
        BattleResultsInteractor,
        provides=Interactor[BattleResultsQuery, list[BattleResult]],
    )

    @provide(scope=Scope.APP)
    def db(self) -> DBS:
        return collections.defaultdict(list)

    hero_factory = provide(HeroFactory)

    battle_connector = provide(
        source=BattleAPIClient, provides=ClientProto, scope=Scope.APP
    )

    scope = Scope.REQUEST

    config = from_context(AppConfig, scope=Scope.APP)

    player_mapper = provide(
        source=PlayerMemoryMapper, provides=PlayersMapper, scope=Scope.APP
    )
    start_battle_interactor = provide(
        StartBattleInteractor, provides=AsyncInteractor[StartBattleDTO, BattleId]
    )
    register_interactor = provide(
        NewPlayerInteractor, provides=Interactor[CreatePlayer, Player]
    )
    get_all_interactor = provide(
        ReadPlayersInteractor, provides=Interactor[GetPlayersQuery, list[Player]]
    )
    get_interactor = provide(
        ReadPlayerInteractor, provides=Interactor[GetPlayerQuery, Player]
    )


def make_container() -> AsyncContainer:
    config = read_config()
    return make_async_container(IoC(), context={AppConfig: config})
