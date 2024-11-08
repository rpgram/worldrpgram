from typing import TypeVar, NewType, Any

MinMax = tuple[int | None, int | None]
T = TypeVar("T", bound=type, contravariant=True)
B = TypeVar("B", bound=Any)
DB = list
PlayerId = NewType("PlayerId", int)
BattleId = NewType("BattleId", int)
