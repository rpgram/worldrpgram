import pytest

from rpgram_setup.domain.economics import Token
from rpgram_setup.domain.exceptions import WorldError


def test_empty(empty_balance):
    assert "nothing" in str(empty_balance)
    empty_balance += Token(20)
    assert "20 Tokens" in str(empty_balance)


def test_ops(start_balance):
    start_balance += Token(100)
    assert "399 Tokens" in str(start_balance)
    start_balance -= Token(50)
    assert "349 Tokens" in str(start_balance)


def test_raises(start_balance):
    with pytest.raises(WorldError):
        start_balance -= Token(300)
    with pytest.raises(AssertionError):
        start_balance -= 100
