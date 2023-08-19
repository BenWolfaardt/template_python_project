import logging

from src.adapters.logger import Logger
from src.utils.settings import Settings, load_settings


class App:
    def __init__(self) -> None:
        self.settings: Settings | None = None
        self.logger: logging.Logger | None = None

    def load_settings(self) -> None:
        self.settings = load_settings()

    def setup_logger(self) -> None:
        self.logger = Logger.setup_logger("Txn_States")

    def initialise_services(self) -> None:
        pass

    def setup_services(self) -> None:
        pass

    def start_services(self) -> None:
        pass

        # TODO gracefully shutdown

    def configure_and_start_service(self) -> None:
        self.load_settings()
        self.setup_logger()
        self.initialise_services()
        self.setup_services()
        self.start_services()
