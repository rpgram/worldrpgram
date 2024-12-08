import datetime
import logging

from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.application.exceptions import NotAuthenticatedError
from rpgram_setup.application.identity import (
    IDProvider,
    NewSessionData,
    SessionData,
    SessionDB,
    SessionManager,
)
from rpgram_setup.domain.protocols.general import Hasher
from rpgram_setup.domain.user_types import PlayerId
from rpgram_setup.infrastructure.consts import SESSION_NAME

logger = logging.getLogger(__name__)


class SessionManagerImpl(SessionManager):
    __cookie_key__: str = SESSION_NAME

    def __init__(self, app_config: AppConfig, hasher: Hasher, db: SessionDB):
        self.new_session: NewSessionData | None = None
        self.db = db
        self.expires_interval_sec = app_config.session_expires_in_sec
        self.hasher = hasher

    def refresh_session(self, old_session: str | None):
        if old_session is None:
            return
        session_data = self.db.get(old_session)
        if session_data is None:
            return
        now = datetime.datetime.utcnow().astimezone(datetime.timezone.utc)
        if session_data.expire_at - now < datetime.timedelta(
            seconds=max(10 * 60, int(0.2 * self.expires_interval_sec))
        ):
            expire_at = now + datetime.timedelta(seconds=self.expires_interval_sec)
            new_session = self._encode(session_data.player_id, expire_at)
            self.db[new_session] = SessionData(expire_at, session_data.player_id)
            self.db.pop(old_session)
            self.new_session = NewSessionData(new_session, expire_at)

    def _encode(self, player_id: PlayerId, expire_at: datetime.datetime) -> str:
        data = f"{player_id}%{expire_at.isoformat()}"
        return self.hasher.hash(data)

    def assign_session(self, player_id: PlayerId):
        expire_at = (
            datetime.datetime.utcnow()
            + datetime.timedelta(seconds=self.expires_interval_sec)
        ).astimezone(datetime.timezone.utc)
        new_session = self._encode(player_id, expire_at)
        self.db[new_session] = SessionData(expire_at, player_id)
        self.new_session = NewSessionData(new_session, expire_at)
        logger.debug("Session assigned to  %s", player_id, extra={"scope": "iam"})


class IDProviderImpl(IDProvider):

    def __init__(self, cookie: str | None, db: SessionDB):
        self.db = db
        self.cookie = cookie

    def authenticated_only(self):
        if self.get_payer_identity() is None:
            raise NotAuthenticatedError

    def get_payer_identity(self) -> PlayerId | None:
        if not self.cookie:
            return None
        data = self.db.get(self.cookie)
        if not data:
            return None
        return data.player_id
