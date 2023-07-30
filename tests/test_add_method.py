from src.models import UserModel, DeleteRequest, SelectRequest, SelectResponse, Response


def test_add_user_success(ws, add_request):
    ws.send_model(add_request)
    add_result: Response = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = add_result.id
    expected_result.method = add_request.method
    expected_result.status = 'success'

    assert expected_result == add_result
