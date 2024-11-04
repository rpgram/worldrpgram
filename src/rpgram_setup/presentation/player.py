from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from rpgram_setup.application.models import PlayerDTO
from rpgram_setup.application.register import NewPlayerInteractor
from rpgram_setup.domain.exceptions import NotUnique, ActionFailed
from rpgram_setup.domain.protocols.data.players import CreatePlayer

router = APIRouter(prefix="/player")


# @router.post('/battle')
# @inject
# async def start_battle(player_id: PlayerId, interactor: FromDishka[]) ->


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    username: str, interactor: FromDishka[NewPlayerInteractor]
) -> PlayerDTO:
    create_player = CreatePlayer(username)
    try:
        return interactor.execute(create_player)
    except NotUnique as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    except ActionFailed:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Some inner problems I guess."
        )
