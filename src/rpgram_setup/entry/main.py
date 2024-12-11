import contextlib

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import setup_dishka as set_dish_stream
from fastapi import FastAPI
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from prometheus_fastapi_instrumentator import Instrumentator

from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.application.identity import SessionDB
from rpgram_setup.domain.exceptions import WorldError
from rpgram_setup.entry.ioc import make_container
from rpgram_setup.infrastructure.logging import configure_logs
from rpgram_setup.presentation.api.auth import user_router
from rpgram_setup.presentation.api.battle import battle_router
from rpgram_setup.presentation.api.equip import equip_router
from rpgram_setup.presentation.api.errors import exceptions_handler
from rpgram_setup.presentation.api.results import results_router
from rpgram_setup.presentation.fs.taker import make_rabbit_router
from rpgram_setup.presentation.hero import hero_router
from rpgram_setup.presentation.middlewares import logging_middleware, session_middleware
from rpgram_setup.presentation.player import player_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logs()
    container = app.state.dishka_container
    fs = await create_faststream(container)
    assert fs.broker
    await fs.broker.start()
    yield
    await fs.broker.close()
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    Instrumentator().instrument(app).expose(app)
    app.exception_handler(WorldError)(exceptions_handler)
    session_db: SessionDB = {}
    app.state.session_db = session_db
    container = make_container(session_db)
    app.include_router(player_router)
    app.include_router(battle_router)
    app.include_router(hero_router)
    app.include_router(results_router)
    app.include_router(user_router)
    app.include_router(equip_router)
    app.middleware("http")(logging_middleware)
    app.middleware("http")(session_middleware)
    setup_dishka(container=container, app=app)
    return app


async def create_faststream(container: AsyncContainer) -> FastStream:
    config = await container.get(AppConfig)
    if config.amqp_dsn:
        broker = RabbitBroker(config.amqp_dsn)
    else:
        broker = RabbitBroker()
    faststream_app = FastStream(broker)
    router = make_rabbit_router(None)
    set_dish_stream(container, faststream_app)
    broker.include_router(router)
    return faststream_app
