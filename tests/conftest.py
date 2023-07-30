import pytest
from websockets.sync.client import connect

from src.factories import UserFactory, AddRequestFactory
from src.models import UserModel, AddRequest
from src.ws_wrapper import WsConnection


@pytest.fixture
def ws() -> WsConnection:
    with connect('ws://127.0.0.1:4000') as websocket:
        ws_wrapper = WsConnection(websocket)
        yield ws_wrapper


@pytest.fixture
def user() -> UserModel:
    return UserFactory.build()


@pytest.fixture
def add_request() -> AddRequest:
    return AddRequestFactory.build()
