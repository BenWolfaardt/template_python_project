from threading import Thread

import uvicorn  # type: ignore

from psycopg2 import DatabaseError

from src.adapters.database.config import Database
from src.adapters.database.sql_store import SQLStore
from src.adapters.logger import Logger
from src.adapters.settings import Settings, load_settings
from src.controllers.api import API
from src.controllers.api_routers.db import parse_init_args_to_router_db
from src.controllers.api_routers.db import router as db_router
from src.core.interactors.api_db_crud import APICRUD
from src.core.interactors.db_crud import DBCRUD
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
        self.db_crud: DBCRUD = None  # type: ignore[assignment]
        self.api_crud: APICRUD = None  # type: ignore[assignment]
        self.api: API = None  # type: ignore[assignment]

        try:
            db = Database(db_config, self.logger)

            db.check_migration_existance()
            db.revision("Instantiation", autogenerate=True) if db.to_instantiate else None
            db.upgrade()

        except DatabaseError:
            self.logger.critical("Database not setup correctly")

        self.logger.info("Instantiating CRUD clients")
        self.db_crud = DBCRUD(self.store)
        self.api_crud = APICRUD(self.store)

        self.logger.info("Instantiating Template Python API Controller")
        self.api = API()

        parse_init_args_to_router_db(self.api_crud, self.logger)

        API_VERSION = "/v1"  # TODO add this to config?

        self.api.server.include_router(db_router, prefix=API_VERSION)

    def start_services(self) -> None:
        self.logger.info("Starting the HTTP server")
        uvicorn_config = self.settings.get_uvicorn_config()

        def run_uvicorn() -> None:
            uvicorn.run(
                self.api.server,
                host=uvicorn_config.host,
                port=uvicorn_config.port,
                log_level=uvicorn_config.log_level,
            )

        uvicorn_thread = Thread(target=run_uvicorn)
        uvicorn_thread.start()

        # TODO gracefully shutdown

    def configure_and_start_service(self) -> None:
        self.setup_services()
        self.start_services()
