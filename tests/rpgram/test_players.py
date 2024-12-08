import pytest
from dishka import AsyncContainer

from rpgram_setup.domain.player import Player
from rpgram_setup.domain.protocols.core import Interactor
from rpgram_setup.domain.protocols.data.players import GetPlayerQuery, GetPlayersQuery

from .data import FAKE_PLAYER
from .fixtures.ioc import async_cont


@pytest.mark.asyncio
async def test_players_getter(async_cont: AsyncContainer):
    interactor = await async_cont.get(Interactor[GetPlayersQuery, list[Player]])
    data = interactor.execute(GetPlayersQuery(0, 0))
    assert data == [FAKE_PLAYER]


@pytest.mark.asyncio
async def test_get_player(async_cont):
    interactor = await async_cont.get(Interactor[GetPlayerQuery, Player])
    data = interactor.execute(GetPlayerQuery(None, FAKE_PLAYER.username))
    assert data == FAKE_PLAYER
