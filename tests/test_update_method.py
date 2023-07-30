from src.models import Response


# TODO add parametrization
def test_update_successful(ws, add_request, update_request):
    ws.send_model(add_request)
    ws.recv_model(Response())

    update_request.name = add_request.name + '_new_name'
    ws.send_model(update_request)
    result = ws.recv_model(Response())

    expected_result = Response()
    expected_result.id = update_request.id
    expected_result.method = update_request.method
    expected_result.status = 'success'

    # TODO add select check that name changed (better make 2 soft asserts, for case when got error but change completed

    assert result == expected_result


# TODO add test that check if phone change possible (maybe also add test that phone can not be set to null and empty str
# TODO add test that phone can not be changed to existing number
