from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.core.models.data import Data


class BaseRequest(BaseModel):
    request_id: str | None = Field(default_factory=lambda: str(uuid4()), alias="request_id")


class CreateRequest(BaseRequest):
    data: Data


class CreateResponse(BaseModel):
    data: Data
    request_id: str


class ReadRequest(BaseRequest):
    id: UUID


class ReadResponse(BaseModel):
    data: Data
    request_id: str


class ReadAllRequest(BaseRequest):
    pass


class ReadAllResponse(BaseModel):
    data: list[Data]
    request_id: str


class UpdateRequest(BaseRequest):
    data: Data


class UpdateResponse(BaseModel):
    data: Data
    request_id: str


class DeleteRequest(BaseRequest):
    id: UUID


class DeleteResponse(BaseModel):
    request_id: str
