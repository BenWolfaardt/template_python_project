import logging

from src.core.ports.logging import Logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
        "RESET": "\033[0m",
    }

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        logger_name = record.name
        msg = super().format(record)
        return f"{self.COLORS[levelname]}[{logger_name}] {msg}{self.COLORS['RESET']}"


class Logger(Logging):
    def __init__(self, name: str = "default") -> None:
        self.logger = self.setup_logger(name)

    @staticmethod
    def setup_logger(logger_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        formatter = ColoredFormatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)
