import abc
import hashlib
import hmac
from typing import Protocol

from rpgram_setup.application.configuration import AppConfig


class Display(Protocol):
    def __str__(self) -> str: ...


class Hasher(Protocol):

    @abc.abstractmethod
    def hash(self, value: str) -> str: ...
