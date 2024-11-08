from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from rpgram_setup.application.players.read import (
    ReadPlayersInteractor,
    ReadPlayerInteractor,
)
from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.user_types import PlayerId
from rpgram_setup.presentation.converters import convert_player_to_dto
from rpgram_setup.presentation.models import PlayerDTO
from rpgram_setup.application.players.register import NewPlayerInteractor
from rpgram_setup.domain.exceptions import NotUnique, ActionFailed
from rpgram_setup.domain.protocols.data.players import (
    CreatePlayer,
    GetPlayersQuery,
    GetPlayerQuery,
)

router = APIRouter(prefix="/player")


# @router.post('/battle')
# @inject
# async def start_battle(player_id: PlayerId, interactor: FromDishka[]) ->


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    username: str, interactor: FromDishka[Interactor[CreatePlayer, Player]]
) -> PlayerDTO:
    create_player = CreatePlayer(username)
    try:
        return convert_player_to_dto(interactor.execute(create_player))
    except NotUnique as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    except ActionFailed:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Some inner problems I guess."
        )


@router.get("")
@inject
async def get_players(
    interactor: FromDishka[Interactor[GetPlayersQuery, list[Player]]],
    limit: int = 0,
    skip: int = 0,
) -> list[PlayerDTO]:
    return [
        convert_player_to_dto(p)
        for p in interactor.execute(GetPlayersQuery(limit, skip))
    ]


@router.get("/by")
@inject
async def get_player(
    interactor: FromDishka[Interactor[GetPlayerQuery, Player]],
    player_id: PlayerId | None = None,
    username: str | None = None,
) -> PlayerDTO:
    if not (player_id or username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No params.")
    if player_id and username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too much params.")
    try:
        return convert_player_to_dto(
            interactor.execute(GetPlayerQuery(player_id, username))
        )
    except ActionFailed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such player.")
