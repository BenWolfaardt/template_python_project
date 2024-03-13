import argparse

from copy import deepcopy
from enum import Enum

from envyaml import EnvYAML
from pydantic import BaseModel

from src.core.models.configs import DBConfig, ExecutionConfig, UvicornConfig
from src.core.ports.settings import SettingsPort


class Environment(str, Enum):
    CONTAINERISED = "containerised"
    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


class InvalidEnvironmentError(argparse.ArgumentTypeError):
    def __init__(self, value: str, choices: list[str]):
        self.value = value
        self.choices = choices
        super().__init__(
            f"You have entered an incorrect choice: {value}. Your options are \"{', '.join(choices)}\""
        )


def _parse_env_arg(value: str) -> str:
    if value not in [e.value for e in Environment]:
        raise InvalidEnvironmentError(value, [e.value for e in Environment])
    return Environment(value)


def load_settings() -> "Settings":
    parser = argparse.ArgumentParser(description="App environment")
    parser.add_argument(
        "--env",
        type=_parse_env_arg,
        help="Configuration environment for the app",
        metavar="ENV",
    )
    cli_args = parser.parse_args()

    yaml_config = EnvYAML(f"configs/{cli_args.env.value}.yml", strict=False)
    return Settings(**yaml_config)


class Settings(SettingsPort, BaseModel):
    execution: ExecutionConfig
    db: DBConfig
    uvicorn: UvicornConfig

    def get_execution_config(self) -> ExecutionConfig:
        return self.execution

    def get_db_config(self) -> DBConfig:
        return self.db

    def get_uvicorn_config(self) -> UvicornConfig:
        return self.uvicorn


if __name__ == "__main__":
    config = load_settings()

    execution_config = config.get_execution_config()
    print(f"Execution Configuration: {execution_config}\n")

    db_config = config.get_db_config()
    print(f"DB Configuration: {db_config}")
    print(f"DB url property: {db_config.url}")

    alembic_config = deepcopy(db_config)
    alembic_config.name = "alembic"
    print(f"Alembic url property: {alembic_config.url}\n")

    uvicorn_config = config.get_uvicorn_config()
    print(f"Uvicorn Configuration: {uvicorn_config}\n")
