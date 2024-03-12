from alembic import context
from sqlalchemy import engine_from_config, pool

from src.adapters.database.base import DeclarativeBase
from src.adapters.database.tables.data import DataRow  # noqa: F401


def run_migrations_online() -> None:
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=DeclarativeBase.metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
