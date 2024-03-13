import argparse
import os

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.util import CommandError
from psycopg2 import DatabaseError  # noqa F401: imported but unused
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils.functions import create_database, database_exists

from src.adapters.database.alembic_config import AlembicConfig
from src.adapters.logger import Logger
from src.adapters.settings import Settings, _parse_env_arg, load_settings
from src.core.models.configs import DBConfig
from src.core.ports.logging import Logging


class Database:
    def __init__(
        self,
        db_config: DBConfig,
        logger: Logging,
    ) -> None:
        self.config: Config = AlembicConfig(db_config.migration_location, db_config.url).create()
        self.db_config = db_config
        self.logger = logger
        self.migrations_exist = False
        self.to_instantiate = False

    def check_migration_existance(self) -> None:
        CURRENT_DIRECTORY = Path(__file__).resolve().parent
        MIGRATIONS_DIRECTORY = CURRENT_DIRECTORY.joinpath("migrations", "versions")

        for filename in os.listdir(MIGRATIONS_DIRECTORY):
            if filename.endswith(".py"):
                self.migrations_exist = True
                self.logger.debug(
                    f"Migrations already exist in {self.db_config.migration_location}, setting 'migrations_exist' flag to 'True'"
                )

        if not self.migrations_exist:
            try:
                self.logger.debug(f"Checking existance of any tables for {self.db_config.name} DB")

                metadata = MetaData()
                metadata.reflect(bind=self.engine)

                if metadata.tables:
                    self.logger.debug(f"Tables for {self.db_config.name} DB already exists")
                else:
                    self.logger.debug(
                        f"Tables for {self.db_config.name} DB do not exist, setting 'to_instantiate' flag to 'True'"
                    )
                    self.to_instantiate = True

            except SQLAlchemyError as e:
                msg = f"{type(e).__name__}, {str(e)}"
                self.logger.error(msg)
                raise SQLAlchemyError(msg)

    def create(self) -> None:
        self.logger.info(f"Creating {self.db_config.name} engine")

        try:
            self.engine = create_engine(self.db_config.url)

            if not database_exists(self.engine.url):
                self.logger.info(f"{self.db_config.name} DB does not exist, creating...")
                create_database(self.engine.url)
            else:
                self.logger.info(f"{self.db_config.name} DB already exists, skipping creation.")

        except CommandError as c_e:
            msg = f"{type(c_e).__name__}, {str(c_e)}"
            self.logger.error(msg)
            raise CommandError(msg)
        except SQLAlchemyError as sql_e:
            msg = f"{type(sql_e).__name__}, {str(sql_e)}"
            self.logger.error(msg)
            raise SQLAlchemyError(msg)

    # alembic revision --autogenerate -m "message"
    def revision(self, message: str, autogenerate: bool = True) -> None:
        self.logger.info(f"Revising {self.db_config.name} DB: {message}")

        try:
            command.revision(self.config, message, autogenerate)

        except CommandError as e:
            if str(e) == "Target database is not up to date.":
                msg = f"{type(e).__name__}, migration has already been run on DB"
                self.logger.warning(msg)
                raise CommandError(msg)
            else:
                msg = f"{type(e).__name__}, {str(e)}"
                self.logger.error(msg)
                raise CommandError(msg)

    # alembic upgrade head
    def upgrade(self) -> None:
        self.logger.info(f"Running migration(s) on {self.db_config.name} DB")

        try:
            command.upgrade(self.config, "head")

        except CommandError as e:
            msg = f"CommandError: {type(e).__name__}, {str(e)}"
            self.logger.error(msg)
            raise CommandError(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Default DB service")
    parser.add_argument(
        "--env",
        type=_parse_env_arg,
        help="Configuration environment for the app",
        metavar="ENV",
    )

    settings: Settings = load_settings()
    logger: Logging = Logger("Database Config")

    db_config = settings.get_db_config()
    db = Database(db_config, logger)

    db.create()
    db.revision("Instantiation", autogenerate=True) if db.to_instantiate else None
    db.upgrade()
