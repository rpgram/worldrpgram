import hashlib
import hmac
import time

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.application.identity import (
    SessionIDManager,
    SessionData,
    SessionValues,
    RSessionIDManager,
    SessionDB,
    IDProvider,
)
from rpgram_setup.domain.user_types import PlayerId


# class InMemorySessionManager(SessionIDManager):
#
#     def __init__(self, expires_interval_sec: int, secret_key: str, session_reader: SessionReader):
#         self.session_reader = session_reader
#         self.secret_key = secret_key
#         self.expires_interval_sec = expires_interval_sec
#         self.db: dict[str, SessionData] = {}
#         self.session_value = None
#         self.identity = None
#         self.new_session_value = None
#
#     def infer_actual_id(self):
#         if self.session_value is None:
#             self.session_value = self.session_reader.rsession_id
#         session_data = self.db.get(self.session_value)
#         if session_data is None:
#             return
#         now = int(time.time())
#         if session_data.expire_at - now < max(
#             10 * 60, int(0.2 * self.expires_interval_sec)
#         ):
#             self.db.pop(self.session_value)
#             rsession_id = self.login(session_data.player_id)
#             self.new_session_value = rsession_id
#         self.identity = session_data.player_id
#
#     def login(self, player_id: PlayerId) -> str:
#         expires_at = int(time.time()) + self.expires_interval_sec
#         rsession_id = self._encode(player_id, expires_at)
#         session_data = SessionData(expires_at, player_id)
#         self.db[rsession_id] = session_data
#         return rsession_id
#
#     def _encode(self, player_id: PlayerId, expires_at: int) -> str:
#         hmac_obj = hmac.new(
#             self.secret_key.encode(),
#             f"{player_id}:{expires_at}".encode(),
#             hashlib.sha256,
#         )
#         return hmac_obj.hexdigest()
#


class RSessionIDManagerImpl(RSessionIDManager):

    def __init__(self, secret_key: str, expires_interval_sec: int, db: SessionDB):
        self.old_session = None
        self.new_session = None
        self.db = db
        self.expires_interval_sec = expires_interval_sec
        self.secret_key = secret_key

    def _encode(self, player_id: PlayerId, expires_at: int) -> str:
        hmac_obj = hmac.new(
            self.secret_key.encode(),
            f"{player_id}:{expires_at}".encode(),
            hashlib.sha256,
        )
        return hmac_obj.hexdigest()

    def refresh_session(self, session_value: str):
        session_data = self.db.get(session_value)
        if session_data is None:
            return
        now = int(time.time())
        if session_data.expire_at - now < max(
            10 * 60, int(0.2 * self.expires_interval_sec)
        ):
            expire_at = now + self.expires_interval_sec
            new_session = self._encode(session_data.player_id, expire_at)
            self.db[new_session] = SessionData(expire_at, session_data.player_id)
            self.db.pop(session_value)
            self.new_session = new_session

    def login(self, player_id: PlayerId):
        expire_at = int(time.time()) + self.expires_interval_sec
        new_session = self._encode(player_id, expire_at)
        self.db[new_session] = SessionData(expire_at, player_id)
        self.new_session = new_session


class IDProviderImpl(IDProvider):

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
