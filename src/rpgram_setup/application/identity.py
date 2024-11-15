import abc
import dataclasses
from typing import Protocol, Any

from fastapi import Cookie

from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass(frozen=True)
class SessionData:
    expire_at: int
    player_id: PlayerId


@dataclasses.dataclass
class SessionValues:
    player_id: PlayerId
    rsession_id: str


class IDProvider(Protocol):

    @abc.abstractmethod
    def get_payer_identity(self) -> PlayerId: ...


class SessionIDManager(Protocol):

    db: Any
    identity: Any | None
    session_value: str | None
    new_session_value: str | None
    __cookie_key__: str = "RSESSION_ID"

    @abc.abstractmethod
    def infer_actual_id(self): ...

    @abc.abstractmethod
    def login(self, player_id: PlayerId): ...


SessionDB = dict[str, SessionData]


class RSessionIDManager(Protocol):
    __cookie_key__: str = "RSESSION_ID"
    db: SessionDB
    old_session: str | None
    new_session: str | None

    @abc.abstractmethod
    def refresh_session(self, session_value: str): ...

    @abc.abstractmethod
    def login(self, player_id: PlayerId): ...
