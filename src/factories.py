from uuid import uuid4

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.models import *


class UserFactory(ModelFactory[UserModel]):
    __model__ = UserModel


class RequestFactory(ModelFactory[Request]):
    __model__ = Request

    @classmethod
    def id(cls) -> str:
        return str(uuid4())


class AddRequestFactory(RequestFactory):
    __model__ = AddRequest

    method = 'add'


class DeleteRequestFactory(RequestFactory):
    __model__ = DeleteRequest

    method = 'delete'


class UpdateRequestFactory(RequestFactory):
    __model__ = UpdateRequest

    method = 'update'


class SelectRequestFactory(RequestFactory):
    __model__ = SelectRequest

    method = 'select'
    name = None
    surname = None
    phone = None
