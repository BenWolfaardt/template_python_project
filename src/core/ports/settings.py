from abc import ABC, abstractmethod

from src.core.models.configs import DBConfig, ExecutionConfig, UvicornConfig


class SettingsPort(ABC):
    @abstractmethod
    def get_db_config(self) -> DBConfig:
        pass

    @abstractmethod
    def get_execution_config(self) -> ExecutionConfig:
        pass

    @abstractmethod
    def get_uvicorn_config(self) -> UvicornConfig:
        pass
