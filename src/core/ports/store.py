from abc import ABC, abstractmethod
from uuid import UUID

from src.core.models.data import Data


class Store(ABC):
    @abstractmethod
    def create(self, data: Data) -> Data:
        pass

    @abstractmethod
    def read(self, id: UUID) -> Data:
        pass

    @abstractmethod
    def read_all(self, id: UUID | None) -> list[Data]:
        pass

    @abstractmethod
    def update(self, data: Data) -> Data:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass
