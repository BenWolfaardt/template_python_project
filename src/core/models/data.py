from dataclasses import field
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class Default:
    pass


class Data(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    data: str = field(default_factory=lambda: str(Default()))
    timestamp_created: datetime = Field(default_factory=datetime.now)
    timestamp_updated: datetime = Field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        sentinel = str(Default())
        for field_name in self.__annotations__:
            if getattr(self, field_name) == sentinel:
                setattr(self, field_name, None)
