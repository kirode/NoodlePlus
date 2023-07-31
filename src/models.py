from __future__ import annotations

from typing import Optional, Literal, List

from pydantic import BaseModel
from uuid import uuid4


class UserModel(BaseModel):
    name: str
    surname: str
    phone: str
    age: int

    def __lt__(self, other: UserModel):
        return self.phone < other.phone

    def __gt__(self, other: UserModel):
        return self.phone > other.phone


class Request(BaseModel):
    id: str = str(uuid4())


class AddRequest(Request, UserModel):
    method: str = 'add'


class DeleteRequest(Request):
    method: str = 'delete'
    phone: str = None


class UpdateRequest(Request):
    method: str = 'update'
    name: Optional[str]
    surname: Optional[str]
    phone: Optional[str]
    age: Optional[int]


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
