from fastapi import Cookie, Depends, HTTPException
from starlette import status

from rpgram_setup.application.exceptions import NotAuthenticated
from rpgram_setup.application.identity import SessionData, SessionDB, IDProvider
from rpgram_setup.infrastructure.session import IDProviderImpl


def auth_db():
    raise NotImplementedError


def id_provider(
    rsession_id=Cookie(None, alias="RSESSION_ID"), db: SessionDB = Depends(auth_db)
) -> IDProviderImpl:
    return IDProviderImpl(rsession_id, db)
