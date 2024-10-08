import json

from enum import Enum

from pydantic import BaseModel


class StoreType(str, Enum):
    MEMORY = "memory"
    SQL = "sql"


class Environment(str, Enum):
    LOCAL = "local"
    CONTAINERISED = "containerised"


class BaseConfig(BaseModel):
    def to_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="json", exclude_none=True),
            sort_keys=True,
            indent=4,
        )


class ExecutionConfig(BaseConfig):
    store_type: StoreType


class DBConfig(BaseConfig):
    user: str
    password: str
    host: str
    port: int
    name: str
    migration_location: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LoggerConfig(BaseConfig):
    name: str
    environment: Environment
    level: str
    output_file: str


class UvicornConfig(BaseConfig):
    host: str
    port: int
    log_level: str
