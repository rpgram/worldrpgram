import random
import string

import pytest

from rpgram_setup.infrastructure.general import HasherImpl
from .app import config


@pytest.fixture
def hasher(config):
    return HasherImpl(config)


def test_hashing(hasher):
    test_value = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(15)
    )
    assert hasher.hash(test_value) == hasher.hash(test_value)
