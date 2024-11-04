import abc
from typing import Protocol, TypeVar, Any

I = TypeVar("I", bound=Any, contravariant=True)
O = TypeVar("O", bound=Any, covariant=True)


class ConnectorProto(Protocol[I, O]):
    @abc.abstractmethod
    async def make_call(self, call_data: I) -> O: ...


class ClientProto(Protocol):
    connector: ConnectorProto

    @abc.abstractmethod
    async def start_battle(self, player, opponent) -> None: ...
