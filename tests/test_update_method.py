import pytest
from pytest_check import check

from helpers import get_user_from_request_model
from src.models import Response, SelectResponse


@pytest.mark.parametrize('key, value', [
    ('name', '_new_name'),
    ('surname', '_new_surname'),
    ('phone', '1234'),
    ('age', 12)
])
def test_update_successful(ws, add_request, update_request, select_request, key, value):
    ws.send_model(add_request)
    ws.recv_model(Response())

    update_request.name = add_request.name
    update_request.surname = add_request.surname
    update_request.phone = add_request.phone
    update_request.age = add_request.age

    vars(update_request)[key] += value
    ws.send_model(update_request)
    result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = update_request.id
    expected_result.method = update_request.method
    expected_result.status = 'success'

    with check:
        assert result == expected_result

    select_request.phone = add_request.phone
    ws.send_model(select_request)
    result = ws.recv_model(SelectResponse())

    expected_user = get_user_from_request_model(add_request)
    vars(expected_user)[key] += value

    with check:
        assert result.users[0] == expected_user


@pytest.mark.parametrize('phone_value', ['', None])
def test_phone_can_not_be_empty(ws, add_request, update_request, select_request, phone_value):
    ws.send_model(add_request)
    ws.recv_model(Response())

    update_request.name = add_request.name
    update_request.surname = add_request.surname
    update_request.phone = phone_value
    update_request.age = add_request.age

    ws.send_model(update_request)
    result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = update_request.id
    expected_result.status = 'failure'
    expected_result.reason = 'phone can not be empty'

    with check:
        assert result == expected_result

    select_request.name = add_request.name
    select_request.surname = add_request.surname
    ws.send_model(select_request)
    result = ws.recv_model(SelectResponse())

    expected_user = get_user_from_request_model(add_request)

    with check:
        assert result.users[0] == expected_user

# TODO add test that phone can not be changed to existing number
