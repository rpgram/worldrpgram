import abc
import math
from typing import Protocol, Self

from rpgram_setup.domain.exceptions import BalanceTooLow
from rpgram_setup.domain.user_types import Ledger


class Currency(Protocol):
    @abc.abstractmethod
    def __add__(self, other) -> Self: ...

    @abc.abstractmethod
    def __sub__(self, other) -> Self: ...

    @abc.abstractmethod
    def __isub__(self, other) -> Self: ...

    @abc.abstractmethod
    def __iadd__(self, other) -> Self: ...

    @abc.abstractmethod
    def mul(self, coefficient: float, *, rize: bool) -> Self: ...

    @abc.abstractmethod
    def __lt__(self, other) -> bool: ...


class Token(Currency):
    def __init__(self, units: int):
        self.units = units

    def __sub__(self, other):
        if not isinstance(other, Token):
            raise NotImplemented
        return Token(self.units - other.units)

    def __add__(self, other):
        if not isinstance(other, Token):
            raise NotImplemented
        return Token(self.units + other.units)

    def __isub__(self, other):
        sub = self.__sub__(other)
        return sub

    def __iadd__(self, other):
        sum_ = self.__add__(other)
        return sum_

    def mul(self, coefficient: float, *, rize: bool) -> Self:
        result = self.units * coefficient
        if rize:
            return self.__class__(math.ceil(result))
        return self.__class__(int(result))


Money = Token


class Balance:
    def __init__(self, ledger: Ledger):
        self.ledger = ledger

    def __iadd__(self, other):
        assert isinstance(other, Money)
        currency_balance = self.ledger.get(type(other))
        if currency_balance is None:
            self.ledger[type(other)] = other
        else:
            self.ledger[type(other)] += other
        return self

    def __isub__(self, other):
        assert isinstance(other, Money)
        if self.ledger.get(type(other)) is None:
            raise NotImplemented
        if self.ledger[type(other)] < other:
            raise BalanceTooLow
        self.ledger[type(other)] -= other
        return self
