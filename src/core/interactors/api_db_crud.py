from dataclasses import dataclass

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

    def create(self, r: CreateRequest) -> CreateResponse:
        return CreateResponse(data=self.store.create(r.data), request_id=r.request_id)

    def read(self, r: ReadRequest) -> ReadResponse:
        return ReadResponse(data=self.store.read(r.id), request_id=r.request_id)

    def read_all(self, r: ReadAllRequest) -> ReadAllResponse:
        return ReadAllResponse(data=self.store.read_all(), request_id=r.request_id)

    def update(self, r: UpdateRequest) -> UpdateResponse:
        return UpdateResponse(data=self.store.update(r.data), request_id=r.request_id)

    def delete(self, r: DeleteRequest) -> DeleteResponse:
        return DeleteResponse(request_id=r.request_id)
