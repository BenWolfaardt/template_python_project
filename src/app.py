import logging

from src.adapters.logger import Logger
from src.utils.settings import Settings, load_settings


class App:
    def __init__(self) -> None:
        self.settings: Settings | None = None
        self._logger: logging.Logger | None = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = Logger.setup_logger("Template")
        return self._logger

    def load_settings(self) -> None:
        self.settings = load_settings()

    def initialise_services(self) -> None:
        pass

    def setup_services(self) -> None:
        pass
        # self.service_x = ServiceX(self.settings.section_1(), self.logger)

    def start_services(self) -> None:
        if self.settings is not None:
            config_section_1 = self.settings.section_1()
            asd = config_section_1["sub_section_1"]["key_1"]
            self.logger.info(f"{asd}")
        else:
            self.logger.info("Settings not loaded")

        # TODO gracefully shutdown

    def configure_and_start_service(self) -> None:
        self.load_settings()
        self.initialise_services()
        self.setup_services()
        self.start_services()
