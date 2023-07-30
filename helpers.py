from src.models import UserModel, AddRequest


def get_user_from_request_model(model: AddRequest) -> UserModel:
    user_data = vars(model)
    user_data.pop('id')
    user_data.pop('method')
    return UserModel.model_validate(user_data)
