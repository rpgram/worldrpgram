import os

from rpgram_setup.application.configuration import AppConfig


def read_config():
    return AppConfig(battle_url=os.environ["BATTLE_URL"])
