import logging

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.domain.exceptions import WorldException, ValidationError, ActionFailed


async def exceptions_handler(request: Request, exc: WorldException):
    et = type(exc)
    if et is NotAuthenticated:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc))
    if et is ValidationError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    if et is ActionFailed:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(exc))
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Unhandled exception")
