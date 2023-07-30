from uuid import uuid4

import pytest

from src.models import UserModel, DeleteRequest, SelectRequest, SelectResponse, Response


def test_add_user_success(ws, add_request):
    ws.send_model(add_request)
    add_result: Response = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_result.id
    expected_result.method = add_request.method
    expected_result.status = 'success'

    assert expected_result == add_result


def test_duplicated_phone(ws, add_request):
    ws.send_model(add_request)
    add_request.id = str(uuid4())

    ws.send_model(add_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_request.id
    expected_result.method = add_request.method
    expected_result.status = 'failure'
    expected_result.reason = 'duplicated phone'

    assert expected_result == failed_result


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

    assert expected_result == add_result


@pytest.mark.parametrize('field', ['id', 'method', 'name', 'surname', 'phone', 'age'])
def test_mandatory_fields_validation(ws, add_request, field):
    delattr(add_request, field)
    ws.send_model(add_request)
    failed_result = ws.recv_model(Response())

    expected_result = Response()
    if field != 'id':
        expected_result.id = add_request.id
    if field != 'method':
        expected_result.method = add_request.method
    expected_result.status = 'failure'
    expected_result.reason = f'{field} missed'

    assert expected_result == failed_result
