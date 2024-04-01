from dataclasses import dataclass
from uuid import UUID

from src.core.models.data import Data
from src.core.ports.store import Store


@dataclass
class DBCRUD:
    store: Store

    def create(self, data: Data) -> Data:
        return self.store.create(data)

    def read(self, uuid: UUID) -> Data:
        return self.store.read(uuid)

    def read_all(self) -> list[Data]:
        return self.store.read_all()

    def update(self, data: Data) -> bool:
        return self.store.update(data)

    def delete(self, uuid: UUID) -> bool:
        return self.store.delete(uuid)
