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

    # TODO don't create the uuid4 at Response level
    def create(self, r: CreateRequest, request_id: str) -> CreateResponse:
        return CreateResponse(data=self.store.create(r.data), request_id=request_id)

    def read(self, r: ReadRequest, request_id: str) -> ReadResponse:
        return ReadResponse(data=self.store.read(r.id), request_id=request_id)

    def read_all(self, r: ReadAllRequest, request_id: str) -> ReadAllResponse:
        return ReadAllResponse(data=self.store.read_all(r.id), request_id=request_id)

    def update(self, r: UpdateRequest, request_id: str) -> UpdateResponse:
        return UpdateResponse(data=self.store.update(r.data), request_id=request_id)

    def delete(self, r: DeleteRequest, request_id: str) -> DeleteResponse:
        return DeleteResponse(success=self.store.delete(r.id), request_id=request_id)
