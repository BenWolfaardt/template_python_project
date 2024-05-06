from dataclasses import dataclass
from uuid import uuid4

from src.core.models.api_routers.db import (
    CreateRequest,
    CreateResponse,
    DeleteRequest,
    DeleteResponse,
    ReadAllRequest,
    ReadAllResponse,
    ReadRequest,
    ReadResponse,
    UpdateRequest,
    UpdateResponse,
)
from src.core.ports.store import Store


@dataclass
class APICRUD:
    store: Store

    # TODO don't create the uuid4 at Response level
    def create(self, r: CreateRequest) -> CreateResponse:
        return CreateResponse(data=self.store.create(r.data), request_id=r.request_id or str(uuid4()))

    def read(self, r: ReadRequest) -> ReadResponse:
        return ReadResponse(data=self.store.read(r.id), request_id=r.request_id or str(uuid4()))

    def read_all(self, r: ReadAllRequest) -> ReadAllResponse:
        return ReadAllResponse(data=self.store.read_all(), request_id=r.request_id or str(uuid4()))

    def update(self, r: UpdateRequest) -> UpdateResponse:
        return UpdateResponse(data=self.store.update(r.data), request_id=r.request_id or str(uuid4()))

    def delete(self, r: DeleteRequest) -> DeleteResponse:
        return DeleteResponse(request_id=r.request_id or str(uuid4()))
