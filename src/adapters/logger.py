import logging

from typing import ClassVar

from fastapi.responses import JSONResponse

from src.adapters.settings import LOGGING_LEVEL_MAPPING
from src.core.models.configs import LoggerConfig
from src.core.ports.logging import Logging, T


class ConsoleFormatter(logging.Formatter):
    # TODO: no exception?
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
        "RESET": "\033[0m",
    }

    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        name = record.name
        msg = super().format(record)
        return f"{self.COLORS[level]}[{name}] {msg}{self.COLORS['RESET']}"


class LokiFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        name = record.name
        msg = super().format(record)
        return f"[{name}] {msg}"


class Logger(Logging):
    def __init__(self, config: LoggerConfig, none_default_name: str | None = None) -> None:
        self.logger = self.setup_logger(config, none_default_name)
        self.errors = self.Exceptions(self)

    class Exceptions(Logging.Exceptions):
        def __init__(self, logger: "Logger") -> None:
            super().__init__()
            self.logger = logger

        def log_exception(
            self,
            message: str,
            exception: T,
        ) -> None:
            msg = f"{type(exception).__name__}: {message}: {exception}"
            self.logger.exception(msg)

        def log_api_exception_and_raise_http_exception(
            self,
            message: str,
            exception: T,
            request_id: str,
            status_code: int,
        ) -> None:
            detail = f"{request_id=}: {message}"
            msg = f"{type(exception).__name__}: {detail}: {exception}"
            self.logger.exception(msg)
            raise JSONResponse(status_code=status_code, content={"error_message": msg})

        def log_critical_and_raise(
            self,
            message: str,
            exception: T,
        ) -> None:
            msg = f"{type(exception).__name__}: {message}: {exception}"
            self.logger.critical(msg)
            raise exception

    @staticmethod
    def setup_logger(config: LoggerConfig, none_default_name: str | None) -> logging.Logger:
        logger = logging.getLogger(none_default_name) if none_default_name else logging.getLogger(config.name)
        logger.setLevel(LOGGING_LEVEL_MAPPING[config.level])

        loki_formatter = LokiFormatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            # TODO: I don't see these in the logs, check Grafana
            defaults={"tags": {"service": config.name, "environment": config.environment}},
        )
        file_handler = logging.FileHandler(config.output_file)
        file_handler.setFormatter(loki_formatter)

        console_formatter = ConsoleFormatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console = logging.StreamHandler()
        console.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console)

        return logger

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def exception(self, msg: str, stack_info: bool = True) -> None:
        self.logger.exception(msg, stack_info=stack_info)

    def critical(
        self,
        msg: str,
        exc_info: bool = True,
        stack_info: bool = True,
    ) -> None:
        self.logger.critical(msg, exc_info=exc_info, stack_info=stack_info)
