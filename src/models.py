from typing import Optional, Literal, List

from pydantic import BaseModel
from uuid import uuid4


class UserModel(BaseModel):
    name: str
    surname: str
    phone: str
    age: int


class Request(BaseModel):
    id: str = str(uuid4())


class AddRequest(Request, UserModel):
    method: str = 'add'


class DeleteRequest(Request):
    method: str = 'delete'
    phone: str = None


class UpdateRequest(Request, UserModel):
    method: str = 'update'


class SelectRequest(Request):
    method: str = 'select'
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None


class Response(BaseModel):
    id: str = None
    method: Literal['add', 'delete', 'update', 'select'] = None
    status: Literal['success', 'failure'] = None
    reason: Optional[str] = None


class SelectResponse(Response):
    users: List[UserModel] = None
