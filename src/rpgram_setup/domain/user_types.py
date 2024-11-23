import collections
from typing import TypeVar, NewType, Any

from rpgram_setup.domain.economics import Money

MinMax = tuple[int | None, int | None]
MinMaxMoney = tuple[Money, Money]
T = TypeVar("T", covariant=True)
B = TypeVar("B", bound=Any)
DBS = collections.defaultdict
PlayerId = NewType("PlayerId", int)
BattleId = NewType("BattleId", int)
