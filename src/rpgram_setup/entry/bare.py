import uvicorn

from rpgram_setup.entry.main import create_app

uvicorn.run(create_app(), port=8001)
