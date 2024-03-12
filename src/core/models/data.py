from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


class Default:
    pass


@dataclass
class Data:
    id: UUID = UUID(int=0x12345678123456781234567812345678)  # TODO update this not to be hardcoded
    data: str = field(default_factory=lambda: str(Default()))
    timestamp_created: datetime = datetime.now()
    timestamp_updated: datetime = datetime.now()

    def __post_init__(self) -> None:
        sentinel = str(Default())
        for field_name in self.__annotations__:
            if getattr(self, field_name) == sentinel:
                setattr(self, field_name, None)
