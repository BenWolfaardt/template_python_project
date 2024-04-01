from datetime import datetime
import json

from typing import Any
from uuid import UUID

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.core.models.data import Data


# TODO think about request ID, maybe assign a default to it?
class CreateRequest(BaseModel):
    data: Data
    request_id: str


class CreateResponse(BaseModel):
    data: Data
    request_id: str


class ReadRequest(BaseModel):
    id: UUID
    request_id: str


class ReadResponse(BaseModel):
    data: Data
    request_id: str


class ReadAllRequest(BaseModel):
    request_id: str


class ReadAllResponse(BaseModel):
    data: list[Data]
    request_id: str


class UpdateRequest(BaseModel):
    data: Data
    request_id: str


class UpdateResponse(BaseModel):
    data: Data
    request_id: str


class DeleteRequest(BaseModel):
    id: UUID
    request_id: str


class DeleteResponse(BaseModel):
    request_id: str
