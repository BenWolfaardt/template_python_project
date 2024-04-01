import json

from pydantic import BaseModel


class BaseConfig(BaseModel):
    def to_json(self) -> str:
        return json.dumps(self.model_dump(mode="json", exclude_none=True), sort_keys=True, indent=4)


# TODO both should be enums
class ExecutionConfig(BaseConfig):
    store_type: str
    logging: str


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


class UvicornConfig(BaseConfig):
    host: str
    port: int
    log_level: str
