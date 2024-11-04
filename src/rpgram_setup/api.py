import contextlib

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from rpgram_setup.infrastructure.ioc import InteractorProvider
from rpgram_setup.presentation.player import router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app():
    container = make_async_container(InteractorProvider())
    app = FastAPI(lifespan=lifespan)
    setup_dishka(container=container, app=app)
    app.include_router(router)
    return app


uvicorn.run(create_app())
