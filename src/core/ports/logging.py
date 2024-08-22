from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar("T", bound=Exception)


class Logging(ABC):
    class Exceptions(ABC):
        @abstractmethod
        def log_exception(
            self,
            message: str,
            exception: Exception,
        ) -> None:
            pass

        @abstractmethod
        def log_api_exception_and_raise_http_exception(
            self,
            message: str,
            exception: T,
            request_id: str,
            status_code: int,
        ) -> None:
            pass

        @abstractmethod
        def log_critical_and_raise(
            self,
            message: str,
            exception: Exception,
        ) -> None:
            pass

    @abstractmethod
    def debug(self, msg: str) -> None:
        pass

    @abstractmethod
    def info(self, msg: str) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str) -> None:
        pass

    @abstractmethod
    def exception(self, msg: str, stack_info: bool = True) -> None:
        pass

    @abstractmethod
    def critical(
        self,
        msg: str,
        exc_info: bool = True,
        stack_info: bool = True,
    ) -> None:
        pass
