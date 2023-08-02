from uuid import uuid4

import pytest
from pytest_check import check

from src.models import UserModel, DeleteRequest, SelectRequest, SelectResponse, Response


def test_add_user_success(ws, add_request):
    ws.send_model(add_request)
    add_result: Response = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_result.id
    expected_result.method = add_request.method
    expected_result.status = 'success'

    assert add_result == expected_result


def test_duplicated_phone(ws, add_request):
    ws.send_model(add_request)
    ws.recv_model(Response())
    add_request.id = str(uuid4())

    ws.send_model(add_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_request.id
    expected_result.status = 'failure'
    expected_result.reason = 'duplicated phone'

    assert failed_result == expected_result


def test_add_empty_phone(ws, add_request):
    add_request.phone = ''
    ws.send_model(add_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_request.id
    expected_result.status = 'failure'
    expected_result.reason = 'phone can not be empty'

    assert failed_result == expected_result


def test_duplicated_data_exclude_phone(ws, add_request):
    ws.send_model(add_request)
    add_request.id = str(uuid4())
    add_request.phone = str(uuid4())

    ws.send_model(add_request)
    add_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_result.id
    expected_result.method = add_request.method
    expected_result.status = 'success'

    assert add_result == expected_result


@pytest.mark.parametrize('field', ['id', 'method', 'name', 'surname', 'phone', 'age'])
def test_mandatory_fields_validation(ws, add_request, field):
    delattr(add_request, field)
    ws.send_model(add_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    if field != 'id':
        expected_result.id = add_request.id
    expected_result.status = 'failure'
    expected_result.reason = f"[json.exception.out_of_range.403] key '{field}' not found"

    assert failed_result == expected_result


@pytest.mark.parametrize('key, value, reason', [
    ('name', 123, '[json.exception.type_error.302] type must be string, but is number'),
    ('surname', 3214, '[json.exception.type_error.302] type must be string, but is number'),
    ('phone', True, '[json.exception.type_error.302] type must be string, but is boolean'),
    ('age', False, '[json.exception.type_error.302] type must be integer, but is boolean')
])
def test_add_invalid_types(ws, add_request, update_request, select_request, key, value, reason):

    vars(add_request)[key] = value
    ws.send_model(add_request)
    result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_request.id
    expected_result.status = 'failure'
    expected_result.reason = reason

    with check:
        assert result == expected_result

    select_request.phone = add_request.phone
    ws.send_model(select_request)
    result = ws.recv_model(SelectResponse())

    with check:
        assert len(result.users) == 0
