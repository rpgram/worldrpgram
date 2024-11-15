import os

from rpgram_setup.application.configuration import AppConfig


def read_config():
    return AppConfig(
        battle_url=os.environ["BATTLE_URL"],
        session_expires_in_sec=120 * 60,
        secret_key="secret_key_for_app",
    )
