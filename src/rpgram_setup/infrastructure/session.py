import datetime
import hashlib
import hmac
import time

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.application.identity import (
    SessionData,
    RSessionIDManager,
    SessionDB,
    IDProvider,
    NewSessionData,
)
from rpgram_setup.domain.user_types import PlayerId


class RSessionIDManagerImpl(RSessionIDManager):

    def __init__(self, secret_key: str, expires_interval_sec: int, db: SessionDB):
        self.new_session: NewSessionData | None = None
        self.db = db
        self.expires_interval_sec = expires_interval_sec
        self.secret_key = secret_key

    def _encode(self, player_id: PlayerId, expires_at: datetime.datetime) -> str:
        hmac_obj = hmac.new(
            self.secret_key.encode(),
            f"{player_id}:{expires_at.isoformat()}".encode(),
            hashlib.sha256,
        )
        return hmac_obj.hexdigest()

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

    def login(self, player_id: PlayerId):
        expire_at = (
            datetime.datetime.utcnow()
            + datetime.timedelta(seconds=self.expires_interval_sec)
        ).astimezone(datetime.timezone.utc)
        new_session = self._encode(player_id, expire_at)
        self.db[new_session] = SessionData(expire_at, player_id)
        self.new_session = NewSessionData(new_session, expire_at)


class IDProviderImpl(IDProvider):

    def authenticated_only(self):
        if self.get_payer_identity() is None:
            raise NotAuthenticated

    def __init__(self, cookie: str | None, db: SessionDB):
        self.db = db
        self.cookie = cookie

    def get_payer_identity(self) -> PlayerId | None:
        if not self.cookie:
            return None
        data = self.db.get(self.cookie)
        if not data:
            return None
        return data.player_id
