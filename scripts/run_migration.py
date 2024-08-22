import argparse

from src.adapters.database.config import Database
from src.adapters.logger import Logger
from src.adapters.settings import Settings, _parse_env_arg, load_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Default DB service")
    parser.add_argument(
        "--env",
        type=_parse_env_arg,
        help="Configuration environment for the app",
        metavar="ENV",
    )
    settings: Settings = load_settings()

    logger_config = settings.get_logger_config()
    logger = Logger(logger_config, "Migration_Script")

    # ------------------ User Input ------------------ #
    db = Database(settings.get_db_config(), logger)  # TODO: select DB if multiple
    migration_message = input("Migration message: ")

    db.upgrade()
    db.revision(migration_message, autogenerate=True)
    db.upgrade()


if __name__ == "__main__":
    main()
