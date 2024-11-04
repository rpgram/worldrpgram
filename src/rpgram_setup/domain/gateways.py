import abc
import dataclasses
from typing import Protocol, Literal, Any, Generic

from rpgram_setup.domain.user_types import T


@dataclasses.dataclass
class RequestData(Generic[T]):
    method: Literal["POST", "GET"]
    api_url: str
    query_params: dict[str, Any]
    return_type: type[T]


class APIGateway(Protocol):

    @abc.abstractmethod
    def _gateway_call(self, request: RequestData[T]) -> T: ...


class BattleGateway(APIGateway):
    # def __init__(self, client):
    #     self._client = client

    def _gateway_call(self, request: RequestData[T]) -> T:
        raise NotImplementedError
