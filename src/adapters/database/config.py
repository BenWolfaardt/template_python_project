import argparse

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
        self.to_instantiate = False

        self.engine = create_engine(self.db_config.url)
        self._check_db_existance()

    def _check_db_existance(self) -> None:
        try:
            self.logger.debug(f"Checking if {self.db_config.name} DB exists")

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
            if not database_exists(self.engine.url):
                self.logger.info(f"{self.db_config.name} DB does not exist, creating...")
                create_database(self.engine.url)

        except CommandError as e:
            msg = f"{type(e).__name__}, {str(e)}"
            self.logger.error(msg)
            raise SQLAlchemyError(msg)

    # alembic revision --autogenerate -m "message"
    def revision(self, message: str, autogenerate: bool = True) -> None:
        self.logger.info(f"Revising {self.db_config.name} DB: {message}")

        try:
            command.revision(self.config, message, autogenerate)

        except CommandError as e:
            msg = f"{type(e).__name__}, {str(e)}"
            self.logger.error(msg)
            raise SQLAlchemyError(msg)

    # alembic upgrade head
    def upgrade(self) -> None:
        self.logger.info(f"Running migration(s) on {self.db_config.name} DB; if any")

        try:
            command.upgrade(self.config, "head")

        except CommandError as e:
            msg = f"CommandError: {type(e).__name__}, {str(e)}"
            self.logger.error(msg)
            raise SQLAlchemyError(msg)


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
