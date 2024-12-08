from rpgram_setup.application.auth import UserLoginDTO, UserRegisterDTO
from rpgram_setup.application.configuration import AppConfig
from rpgram_setup.domain.economics import Balance
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.user import User
from rpgram_setup.domain.user_types import PlayerId

NEW_LOGIN = "NewLogin"
HASH = "caffee"

FAKE_PLAYER = Player(Balance({}), [], [], "PyTester", PlayerId(1))

FAKE_USER = User(PlayerId(1), login="Login", password_hash=HASH, telegram_id=None)

USER_DATA = UserRegisterDTO(username="PyTester", login=NEW_LOGIN, password="VeryS3cure!")

USER_LOGIN = UserLoginDTO("Login", password="ANY")

APP_CONFIG = AppConfig("", 10, "", "", "")
