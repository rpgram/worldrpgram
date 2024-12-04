import random
import string

import pytest

from rpgram_setup.application.auth import UserRegisterDTO, UserLoginDTO
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.user import User

from rpgram_setup.infrastructure.general import HasherImpl
from .data import APP_CONFIG, USER_DATA, USER_LOGIN, FAKE_USER
from .fixtures.ioc import async_cont


@pytest.fixture
def hasher():
    return HasherImpl(APP_CONFIG)


def test_hashing(hasher):
    test_value = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(15)
    )
    assert hasher.hash(test_value) == hasher.hash(test_value)


@pytest.mark.asyncio
async def test_registration(async_cont):
    interactor = await async_cont.get(Interactor[UserRegisterDTO, User])
    data = interactor.execute(USER_DATA)
    assert data


@pytest.mark.asyncio
async def test_login(async_cont):
    interactor = await async_cont.get(Interactor[UserLoginDTO, User])
    data = interactor.execute(USER_LOGIN)
    assert data == FAKE_USER
