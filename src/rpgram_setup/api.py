import contextlib

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from rpgram_setup.infrastructure.ioc import make_container
from rpgram_setup.presentation.player import router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app():
    container = make_container()
    app = FastAPI(lifespan=lifespan)
    setup_dishka(container=container, app=app)
    app.include_router(router)
    return app


uvicorn.run(create_app())
