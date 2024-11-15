import pytest

from rpgram_setup.application.configuration import AppConfig


@pytest.fixture
def config():
    return AppConfig("http://localhost:8000", 10_000, "secret")
