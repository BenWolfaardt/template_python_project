from pydantic import BaseModel


# TODO both should be enums
class ExecutionConfig(BaseModel):
    store_type: str
    logging: str


class DBConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str
    migration_location: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class UvicornConfig(BaseModel):
    host: str
    port: int
    log_level: str
