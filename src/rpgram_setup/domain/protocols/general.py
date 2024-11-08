from typing import Protocol


class Display(Protocol):
    def __str__(self) -> str: ...
