from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from rpgram_setup.application.auth import UserRegisterDTO
from rpgram_setup.domain.exceptions import NotUnique
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.user import User
from rpgram_setup.presentation.models import UserDTO

user_router = APIRouter(prefix="/user")


@user_router.post("")
@inject
async def register_user(
    registration_data: UserRegisterDTO,
    interactor: FromDishka[Interactor[UserRegisterDTO, User]],
) -> UserDTO:
    try:
        return UserDTO(interactor.execute(registration_data).login)
    except NotUnique as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
