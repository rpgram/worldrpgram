import os

from rpgram_setup.application.configuration import AppConfig


def read_config():
    return AppConfig(
        battle_url=os.environ["BATTLE_URL"],
        session_expires_in_sec=360 * 60,
        secret_key="secret_key_for_app",
        ch_dsn="clickhouse://localhost:9000/rpgram"
    )
