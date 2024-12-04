import abc
import dataclasses
import datetime
from typing import Protocol


from rpgram_setup.domain.user_types import PlayerId


@dataclasses.dataclass(frozen=True)
class SessionData:
    expire_at: datetime.datetime
    player_id: PlayerId


@dataclasses.dataclass
class NewSessionData:
    rsession_id: str
    expires_at: datetime.datetime


class IDProvider(Protocol):

    @abc.abstractmethod
    def authenticated_only(self): ...

    @abc.abstractmethod
    def get_payer_identity(self) -> PlayerId | None: ...


SessionDB = dict[str, SessionData]


class RSessionIDManager(Protocol):
    __cookie_key__: str = "RSESSION_ID"
    db: SessionDB
    new_session: NewSessionData | None

    @abc.abstractmethod
    def refresh_session(self, old_session: str | None): ...

    @abc.abstractmethod
    def assign_session(self, player_id: PlayerId): ...
