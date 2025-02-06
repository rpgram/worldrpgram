import contextvars
from typing import Any, Mapping, Callable, Awaitable

from starlette.requests import Request
from starlette.responses import Response
from uuid_extensions import uuid7

from rpgram_setup.application.identity import IDProvider, SessionManager


async def session_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response: Response = await call_next(request)
    idm = await request.state.dishka_container.get(SessionManager)
    old_session = request.cookies.get(idm.__cookie_key__)
    idm.refresh_session(old_session)
    if idm.new_session and old_session != idm.new_session.rsession_id:
        response.set_cookie(
            idm.__cookie_key__,
            idm.new_session.rsession_id,
            expires=idm.new_session.expires_at,
        )
    return response


log_context: contextvars.ContextVar[Mapping[str, Any]] = contextvars.ContextVar("logs")


async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    idp: IDProvider = await request.state.dishka_container.get(IDProvider)
    player_id = idp.get_payer_identity()
    log_context.set({"player_id": player_id, "request_id": request.state.request_id})
    response: Response = await call_next(request)
    return response


async def request_id_middleware(
    req: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    req.state.request_id = uuid7()
    return await call_next(req)
