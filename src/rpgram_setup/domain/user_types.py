import collections
from typing import TypeVar, NewType, Any

MinMax = tuple[int | None, int | None]
T = TypeVar("T", covariant=True)
B = TypeVar("B", bound=Any)
DBS = collections.defaultdict
PlayerId = NewType("PlayerId", int)
BattleId = NewType("BattleId", int)
