from typing import TypeVar, NewType

MinMax = tuple[int | None, int | None]
T = TypeVar("T", bound=type)
PlayerId = NewType("PlayerId", int)
BattleId = NewType("BattleId", int)
