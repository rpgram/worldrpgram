import dataclasses
from typing import Any, Generic, Literal

from rpgram_setup.domain.user_types import R


@dataclasses.dataclass(frozen=True)
class RequestData(Generic[R]):
    method: Literal["POST", "GET"]
    api_url: str
    query_params: dict[str, Any] | None
    body: Any | None
    return_type: type[R]


#
# class APIGateway(Protocol):
#
#     @abc.abstractmethod
#     def _gateway_call(self, request: RequestData[T]) -> T: ...
