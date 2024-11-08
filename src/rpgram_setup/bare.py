import uvicorn

from rpgram_setup.api import create_app

uvicorn.run(create_app(), port=8001)
