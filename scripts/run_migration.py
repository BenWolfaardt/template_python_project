import argparse
from src.adapters.database.config import Database
from src.adapters.logger import Logger

from src.adapters.settings import Settings, _parse_env_arg, load_settings
from src.core.ports.logging import Logging
from alembic.util import CommandError  # noqa F401: imported but unused


def main() -> None:
    parser = argparse.ArgumentParser(description="Default DB service")
    parser.add_argument(
        "--env",
        type=_parse_env_arg,
        help="Configuration environment for the app",
        metavar="ENV",
    )
    settings: Settings = load_settings()
    logger: Logging = Logger("Migration Script")

    # ------------------ User Input ------------------ #
    db = Database(settings.get_db_config(), logger)  # select DB if multiple
    migration_message = input("Migration message: ")

    db.create()
    db.upgrade()
    try:
        db.revision(migration_message, autogenerate=True)
    except CommandError as e:
        if str(e) == "Target database is not up to date.":
            db.logger.warning(f"{type(e).__name__}, migration has already been run on DB")
        else:
            db.logger.critical(f"Error performing revision: {type(e).__name__}, {str(e)}")
    db.upgrade()


if __name__ == "__main__":
    main()
