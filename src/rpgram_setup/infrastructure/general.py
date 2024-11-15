import hashlib
import hmac

from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.domain.protocols.general import Hasher


class HasherImpl(Hasher):
    def __init__(self, app_config: AppConfig):
        self.secret = app_config.secret_key

    def hash(self, value: str) -> str:
        hmac_obj = hmac.new(
            self.secret.encode(),
            value.encode(),
            hashlib.sha256,
        )
        return hmac_obj.hexdigest()
