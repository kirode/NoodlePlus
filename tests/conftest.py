import pytest
from websockets.sync.client import ClientConnection, connect

from src.models import UserModel
from src.ws_wrapper import WsConnection


@pytest.fixture
def ws() -> WsConnection:
    with connect('ws:127.0.0.1:4000') as websocket:
        ws_wrapper = WsConnection(websocket)
        yield ws_wrapper


@pytest.fixture
def user():
    return UserModel()
