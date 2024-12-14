import abc
from typing import Protocol


class Display(Protocol):
    def __str__(self) -> str: ...


class Hasher(Protocol):
    @abc.abstractmethod
    def hash(self, value: str) -> str: ...
