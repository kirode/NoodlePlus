from src.models import UserModel, DeleteRequest, SelectRequest, SelectResponse


def test_model_ser():
    data = '{"id": "123123", "method": "select", "status": "success", "users": [{"name": "Peter", "surname": "Vasiliev", "phone": "1235423", "age": 12}]}'
    model = SelectResponse().model_validate_json(data)
    dt = UserModel()
    print(model)
