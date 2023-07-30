import pytest
from websockets.sync.client import connect

from src.factories import UserFactory, AddRequestFactory, DeleteRequestFactory, UpdateRequestFactory
from src.models import UserModel, AddRequest, DeleteRequest, UpdateRequest
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


@pytest.fixture
def delete_request() -> DeleteRequest:
    return DeleteRequestFactory.build()


@pytest.fixture
def update_request() -> UpdateRequest:
    return UpdateRequestFactory.build()
