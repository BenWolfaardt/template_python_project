from uuid import UUID

from pydantic import BaseModel

from src.core.models.data import Data


class BaseResponse(BaseModel):
    request_id: str


class CreateRequest(BaseModel):
    data: Data


class CreateResponse(BaseResponse):
    data: Data


class ReadRequest(BaseModel):
    id: UUID


class ReadResponse(BaseResponse):
    data: Data


class ReadAllRequest(BaseModel):
    id: UUID | None  # TODO: shouldn't use id as it is a reserved keyword


class ReadAllResponse(BaseResponse):
    data: list[Data]


class UpdateRequest(BaseModel):
    data: Data


class UpdateResponse(BaseResponse):
    data: Data


class DeleteRequest(BaseModel):
    id: UUID


class DeleteResponse(BaseResponse):
    success: bool
