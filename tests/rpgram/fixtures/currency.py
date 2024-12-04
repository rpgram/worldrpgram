import pytest

from rpgram_setup.domain.economics import Balance, Token


@pytest.fixture
def empty_balance():
    return Balance({})


@pytest.fixture
def start_balance():
    return Balance({Token: Token(299)})
