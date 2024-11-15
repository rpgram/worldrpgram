from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.domain.exceptions import WorldException


async def exceptions_handler(request: Request, exc: WorldException):
    if type(exc) is NotAuthenticated:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc))
