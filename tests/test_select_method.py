from uuid import uuid4

from helpers import get_user_from_request_model
from src.models import Response, SelectResponse


def test_select_successful(ws, add_request, select_request):
    ws.send_model(add_request)
    ws.recv_model(Response())

    select_request.phone = add_request.phone
    ws.send_model(select_request)
    result = ws.recv_model(SelectResponse())

    expected_result = SelectResponse()
    expected_result.id = select_request.id
    expected_result.method = select_request.method
    expected_result.status = 'success'
    user = get_user_from_request_model(add_request)
    expected_result.users = [user]

    assert result == expected_result


def test_select_few_users_by_name(ws, add_request, select_request):
    ws.send_model(add_request)
    ws.recv_model(Response())
    first_user = get_user_from_request_model(add_request)

    add_request.surname = str(uuid4())
    add_request.id = str(uuid4())
    add_request.phone = str(uuid4())
    ws.send_model(add_request)
    ws.recv_model(Response())
    second_user = get_user_from_request_model(add_request)

    select_request.name = add_request.name
    ws.send_model(select_request)
    result = ws.recv_model(SelectResponse())

    expected_result = SelectResponse()
    expected_result.id = select_request.id
    expected_result.method = select_request.method
    expected_result.status = 'success'
    expected_result.users = sorted([first_user, second_user])

    assert result == expected_result
