from starlette.requests import Request
from starlette.responses import Response

from rpgram_setup.application.identity import RSessionIDManager


async def session_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    idm = await request.state.dishka_container.get(RSessionIDManager)
    old_session = request.cookies.get(idm.__cookie_key__)
    idm.refresh_session(old_session)
    if idm.new_session and old_session != idm.new_session.rsession_id:
        response.set_cookie(
            idm.__cookie_key__,
            idm.new_session.rsession_id,
            expires=idm.new_session.expires_at,
        )
    return response
