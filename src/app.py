from alembic.util import CommandError  # noqa F401: imported but unused
from psycopg2 import DatabaseError

from src.adapters.database.sql_store import SQLStore
from src.adapters.logger import Logger
from src.adapters.settings import Settings, load_settings
from src.core.models.configs import DBConfig
from src.core.ports.logging import Logging


class App:
    def __init__(self) -> None:
        self.settings: Settings = load_settings()
        self.logger: Logging = Logger()
        self.store: SQLStore = None  # type: ignore[assignment]

    def setup_services(self) -> None:
        self.logger.info("Starting Template Service")

        self.logger.info(f"Instantiating communication with the {SQLStore.__name__} DB")
        db_config: DBConfig = self.settings.get_db_config()
        self.store = SQLStore(db_config.url, self.logger)

        try:
            from src.adapters.database.config import Database

            db = Database(db_config, self.logger)

            db.check_migration_existance()
            db.revision("Instantiation", autogenerate=True) if db.to_instantiate else None
            db.upgrade()

        except DatabaseError:
            self.logger.critical("Migrations failed")

        while True:
            pass

    def start_services(self) -> None:
        pass  # TODO gracefully shutdown

    def configure_and_start_service(self) -> None:
        self.setup_services()
        self.start_services()
