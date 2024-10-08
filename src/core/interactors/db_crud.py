from dataclasses import dataclass
from uuid import UUID

from src.core.models.data import Data
from src.core.ports.store import Store


@dataclass
class DBCRUD:
    store: Store

    def create(self, data: Data) -> Data:
        return self.store.create(data)

    def read(self, id: UUID) -> Data:
        return self.store.read(id)

    def read_all(self, id: UUID | None) -> list[Data]:
        return self.store.read_all(id)

    def update(self, data: Data) -> Data:
        return self.store.update(data)

    def delete(self, id: UUID) -> bool:
        return self.store.delete(id)
