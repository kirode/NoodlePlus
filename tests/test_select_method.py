from uuid import uuid4

import pytest

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


@pytest.mark.parametrize('field', ['name', 'surname'])
def test_select_few_users_by_names(ws, add_request, select_request, field):
    ws.send_model(add_request)
    ws.recv_model(Response())
    first_user = get_user_from_request_model(add_request)

    add_request.id = str(uuid4())
    add_request.phone = str(uuid4())
    if field == 'name':
        add_request.surname = str(uuid4())
    if field == 'surname':
        add_request.name = str(uuid4())

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


@pytest.mark.parametrize('param', ['name', 'surname', 'phone'])
def test_select_not_existing_user(ws, select_request, param):
    vars(select_request)[param] = str(uuid4())

    ws.send_model(select_request)
    result = ws.recv_model(SelectResponse())

    expected_result = SelectResponse()
    expected_result.id = select_request.id
    expected_result.status = 'failure'
    expected_result.reason = 'user not found'
    expected_result.users = []

    assert result == expected_result
