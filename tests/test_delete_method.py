from uuid import uuid4

import pytest
from pytest_check import check

from helpers import get_user_from_request_model
from src.models import Request, Response, SelectResponse


def test_successful_delete(ws, add_request, delete_request):
    ws.send_model(add_request)
    ws.recv_model(Request())

    delete_request.phone = add_request.phone
    ws.send_model(delete_request)
    result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = delete_request.id
    expected_result.method = delete_request.method
    expected_result.status = 'success'

    assert result == expected_result


def test_delete_error_phone_not_found(ws, delete_request):
    delete_request.phone = str(uuid4())
    ws.send_model(delete_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = delete_request.id
    expected_result.status = 'failure'
    expected_result.reason = 'phone not found'

    assert failed_result == expected_result


def test_delete_error_no_phone_given(ws, delete_request):
    ws.send_model(delete_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = delete_request.id
    expected_result.status = 'failure'
    expected_result.reason = f"[json.exception.out_of_range.403] key phone not found"

    assert failed_result == expected_result


def test_delete_error_empty_phone(ws, delete_request):
    delete_request.phone = ''
    ws.send_model(delete_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = delete_request.id
    expected_result.status = 'failure'
    expected_result.reason = "phon can not be empty"

    assert failed_result == expected_result


# TODO add test, try to delete with names/age and check user not deleted with select

@pytest.mark.parametrize('field_name', ['name', 'surname', 'age'])
def test_error_with_not_phone_params(ws, add_request, select_request, delete_request, field_name):
    ws.send_model(add_request)
    ws.recv_model(Request())
    user = get_user_from_request_model(add_request)

    vars(delete_request)[field_name] = vars(add_request)[field_name]

    expected_result = Response()
    expected_result.id = delete_request.id
    expected_result.status = 'failure'
    expected_result.reason = "phone is required"

    ws.send_model(delete_request)
    response = ws.recv_model(Response())

    with check:
        assert response == expected_result

    select_request.phone = add_request.phone
    ws.send_model(select_request)
    select_result = ws.recv_model(SelectResponse())

    with check:
        assert select_result.users[0] == user
