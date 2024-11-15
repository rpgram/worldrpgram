import contextlib

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from rpgram_setup.application.identity import SessionDB
from rpgram_setup.infrastructure.dependencies import auth_db
from rpgram_setup.infrastructure.ioc import make_container
from rpgram_setup.presentation.api.results import results_router
from rpgram_setup.presentation.battle import battle_router
from rpgram_setup.presentation.fs.taker import make_rabbit_router
from rpgram_setup.presentation.hero import hero_router
from dishka.integrations.faststream import setup_dishka as set_dish_stream

from rpgram_setup.presentation.middlewares import session_middleware
from rpgram_setup.presentation.player import player_router


session_db: SessionDB = {}
container = make_container(session_db)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    fs = create_faststream(container)
    assert fs.broker
    app.dependency_overrides[auth_db] = lambda: session_db
    await fs.broker.start()
    yield
    await fs.broker.close()
    await app.state.dishka_container.close()


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(player_router)
    app.include_router(battle_router)
    app.include_router(hero_router)
    app.include_router(results_router)
    setup_dishka(container=container, app=app)
    app.middleware("http")(session_middleware)
    return app


def create_faststream(container: AsyncContainer) -> FastStream:
    broker = RabbitBroker()
    faststream_app = FastStream(broker)
    router = make_rabbit_router(None)
    set_dish_stream(container, faststream_app)
    broker.include_router(router)
    return faststream_app
