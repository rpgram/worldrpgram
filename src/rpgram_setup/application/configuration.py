import dataclasses


@dataclasses.dataclass
class AppConfig:
    battle_url: str
    session_expires_in_sec: int
    secret_key: str
    ch_dsn: str
