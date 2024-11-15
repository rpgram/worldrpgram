from starlette.requests import Request
from starlette.responses import Response

from rpgram_setup.application.identity import SessionIDManager, RSessionIDManager


async def session_middleware(request: Request, call_next):
    # ctx = request.app.state.dishka_container

    # async with request.app.state.dishka_container() as ctx:
    # idm = await ctx.get(SessionIDManager)
    # idm: SessionIDManager = await request.state.dishka_container.get(SessionIDManager)
    #     rsession_id = request.cookies.get(idm.__cookie_key__)
    response: Response = await call_next(request)
    idm = await request.state.dishka_container.get(RSessionIDManager)
    if idm.new_session and idm.old_session != idm.new_session:
        response.set_cookie(idm.__cookie_key__, idm.new_session)
    return response
