from src.factories import RequestFactory, AddRequestFactory, SelectRequestFactory
from src.models import UserModel, DeleteRequest, SelectRequest, SelectResponse, Response


def test_add_user_success(ws, add_request):
    ws.send_model(add_request)
    add_result: Response = ws.recv_model(Response())

    assert add_result.id == add_request.id
    assert add_result.method == add_request.method
    assert add_result.status == 'success'
