import abc
import math
from typing import Protocol, Self

from rpgram_setup.domain.exceptions import BalanceTooLow


class Currency(Protocol):
    @abc.abstractmethod
    def __add__(self, other: object) -> Self: ...

    @abc.abstractmethod
    def __sub__(self, other: object) -> Self: ...

    @abc.abstractmethod
    def __isub__(self, other: object) -> Self: ...

    @abc.abstractmethod
    def __iadd__(self, other: object) -> Self: ...

    @abc.abstractmethod
    def __le__(self, other: object) -> bool: ...

    @abc.abstractmethod
    def mul(self, coefficient: float, *, rize: bool) -> Self: ...

    @abc.abstractmethod
    def __lt__(self, other: object) -> bool: ...

    @abc.abstractmethod
    def __str__(self) -> str: ...


Ledger = dict[type[Currency], Currency]


class Token(Currency):

    def __init__(self, units: int):
        self.units = units

    def __str__(self) -> str:
        return f"{self.units} Tokens"

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return self.units <= other.units

    def __sub__(self, other: object) -> Self:
        if not isinstance(other, Token):
            return NotImplemented
        return self.__class__(self.units - other.units)

    def __add__(self, other: object) -> Self:
        if not isinstance(other, Token):
            return NotImplemented
        return self.__class__(self.units + other.units)

    def __isub__(self, other: object) -> Self:
        sub = self.__sub__(other)
        return sub

    def __iadd__(self, other: object) -> Self:
        sum_ = self.__add__(other)
        return sum_

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return self.units < other.units

    def mul(self, coefficient: float, *, rize: bool) -> Self:
        result = self.units * coefficient
        if rize:
            return self.__class__(math.ceil(result))
        return self.__class__(int(result))


Money = Token


class Balance:
    def __init__(self, ledger: Ledger):
        self.ledger = ledger

    def __iadd__(self, other: object) -> Self:
        assert isinstance(other, Money)
        currency_balance = self.ledger.get(type(other))
        if currency_balance is None:
            self.ledger[type(other)] = other
        else:
            self.ledger[type(other)] += other
        return self

    def __isub__(self, other: object) -> Self:
        assert isinstance(other, Money)
        if self.ledger.get(type(other)) is None:
            return NotImplemented
        if self.ledger[type(other)] < other:
            raise BalanceTooLow
        self.ledger[type(other)] -= other
        return self

    def __str__(self) -> str:
        reprs = ", ".join(map(str, self.ledger.values())) if self.ledger else "nothing"
        return f"You have... {reprs}."
