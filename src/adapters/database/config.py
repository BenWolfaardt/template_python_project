import argparse
import os

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.util import CommandError

from src.adapters.database.alembic_config import AlembicConfig
from src.adapters.logger import Logger
from src.adapters.settings import Settings, _parse_env_arg, load_settings
from src.core.models.configs import DBConfig


class Database:
    def __init__(
        self,
        db_config: DBConfig,
        logger: Logger,
    ) -> None:
        self.config: Config = AlembicConfig(db_config.migration_location, db_config.url).create()
        self.db_config = db_config
        self.logger = logger
        self.exceptions = logger.Exceptions(logger)
        self.to_instantiate = True

    def check_migration_existance(self) -> None:
        CURRENT_DIRECTORY = Path(__file__).resolve().parent
        MIGRATIONS_DIRECTORY = CURRENT_DIRECTORY.joinpath("migrations", "versions")

        for filename in os.listdir(MIGRATIONS_DIRECTORY):
            if filename.endswith(".py"):
                self.to_instantiate = False
                self.logger.debug(
                    f"Migrations already exist in {self.db_config.migration_location}, setting 'to_instantiate' flag to 'False'"
                )

    # DB is created directly from the PostgreSQL Docker container
    # def create(self) -> None:

    # alembic revision --autogenerate -m "message"
    def revision(self, message: str, autogenerate: bool = True) -> None:
        self.logger.info(f"Revising {self.db_config.name} DB: {message}")

        try:
            command.revision(self.config, message, autogenerate)

        except CommandError as e:
            if str(e) == "Target database is not up to date.":
                msg = f"{type(e).__name__}, migration has already been run on DB"
                self.logger.warning(msg)
            else:
                msg = f"{type(e).__name__}, {e!s}"
                self.logger.exception(msg)
                raise CommandError(msg) from e

    # alembic upgrade head
    def upgrade(self) -> None:
        self.logger.info(f"Running migration(s) on {self.db_config.name} DB")

        try:
            command.upgrade(self.config, "head")

        except CommandError as e:
            msg = f"CommandError: {type(e).__name__}, {e!s}"
            self.logger.exception(msg)
            raise CommandError(msg) from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Default DB service")
    parser.add_argument(
        "--env",
        type=_parse_env_arg,
        help="Configuration environment for the app",
        metavar="ENV",
    )

    settings: Settings = load_settings()

    logger_config = settings.get_logger_config()
    logger = Logger(logger_config, "Manual_Database_Config")

    db_config = settings.get_db_config()
    db = Database(db_config, logger)

    db.revision("Instantiation", autogenerate=True) if db.to_instantiate else None
    db.upgrade()
