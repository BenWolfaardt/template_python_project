import argparse
import logging
import sys

from pathlib import Path

from envyaml import EnvYAML

from txns.common.adapters.logging import Logging
from txns.open_and_closed.open_and_closed import TxnOpenAndClosed
from txns.send_and_confirm.send_and_confirm import TxnSendAndConfirm


class App:
    def __init__(self) -> None:
        # TODO is this the correct type?
        self.cli_args: argparse.Namespace | None = None
        self.config_path: Path | None = None
        self.settings: EnvYAML | None = None
        self.txn_send_and_confirm: TxnSendAndConfirm | None = None
        self.txn_open_and_closed: TxnOpenAndClosed | None = None
        self.logger: logging.Logger | None = None

    def parse_cli_args(self) -> None:
        parser = argparse.ArgumentParser(description="Txns DB service")
        parser.add_argument(
            "config_path",
            metavar="config_path",
            type=Path,
            help="Path to config in /configs",
        )
        self.cli_args = parser.parse_args()
        self.config_path = self.cli_args.config_path
        if not self.config_path.is_file():
            print(f"Configuration file: {self.config_path} not found")
            sys.exit(1)

    def load_settings(self) -> EnvYAML:
        self.settings = EnvYAML(str(self.config_path), strict=False)
        return self.settings

    def setup_logger(self) -> logging.Logger:
        self.logger = Logging.setup_logger("Txn_States")
        return self.logger

    def initialise_services(self) -> None:
        self.txn_send_and_confirm = TxnSendAndConfirm(self.settings, self.logger)
        self.txn_open_and_closed = TxnOpenAndClosed(self.settings, self.logger)

    def setup_services(self) -> None:
        self.txn_send_and_confirm.setup_service()
        self.txn_open_and_closed.setup_service()

    def start_services(self) -> None:
        self.txn_send_and_confirm.start_service()
        self.txn_open_and_closed.start_service()

        # TODO gracefully shutdown

    def configure_and_start_service(self) -> None:
        self.parse_cli_args()
        self.load_settings()
        self.setup_logger()
        self.initialise_services()
        self.setup_services()
        self.start_services()
