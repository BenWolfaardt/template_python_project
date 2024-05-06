import time

from collections.abc import Generator
from contextlib import contextmanager
from uuid import UUID

from psycopg2 import errors
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.adapters.database.tables.data import DataRow
from src.core.models.data import Data
from src.core.models.exceptions import DataAlreadyExists, DataEmpty, DataIDNotFound
from src.core.ports.logging import Logging
from src.core.ports.store import Store


UniqueViolation = errors.lookup("23505")


class SQLStore(Store):
    def __init__(self, connection_url: str, logger: Logging) -> None:
        self.engine = create_engine(connection_url)
        self.session = sessionmaker(self.engine)
        self.logger = logger

    def create(self, database: Data) -> Data:
        timestamp = time.ctime()

        with self.write_session() as session:
            try:
                row_insert = self._data_to_data_row(database)
                session.add(row_insert)
                session.flush()

                self.logger.info(f"{row_insert.id} successfully written to the Data DB at {timestamp}")

            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    raise DataAlreadyExists(row_insert.id) from e
                else:
                    self.logger.error(
                        f"{row_insert.id} unsuccessfully written to the Data  DB at {timestamp}: {e}"
                    )
                    raise

            else:
                return database

    def read(self, id: UUID) -> Data:
        with self.read_session() as session:
            row = session.query(DataRow).filter_by(id=id).first()
            if not row:
                raise DataIDNotFound(id)
            return self._data_row_to_data(row)

    def read_all(self) -> list[Data]:
        with self.read_session() as session:
            rows = session.query(DataRow).all()
            if not rows:
                raise DataEmpty
            return [self._data_row_to_data(row) for row in rows]

    def update(self, database: Data) -> Data:
        with self.write_session() as session:
            row = session.query(DataRow).filter_by(id=database.id).first()

            if not row:
                raise DataIDNotFound(database.id)

            row_update = self._data_to_data_row(database)

            session.merge(row_update)
            session.flush()

            return database

    def delete(self, id: UUID) -> None:
        with self.write_session() as session:
            row = session.query(DataRow).filter_by(id=id).first()

            if not row:
                raise DataIDNotFound(id)

            session.delete(row)

    @contextmanager
    def write_session(self) -> Generator:
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def read_session(self) -> Generator:
        session = self.session()
        try:
            yield session
        finally:
            session.close()

    @staticmethod
    def _data_to_data_row(
        database: Data,
    ) -> DataRow:
        return DataRow(
            id=database.id,
            data=database.data,
            timestamp_created=database.timestamp_created,
            timestamp_updated=database.timestamp_updated,
        )

    @staticmethod
    def _data_row_to_data(row: DataRow) -> Data:
        return Data(
            id=row.id,
            data=row.data,
            timestamp_created=row.timestamp_created,
            timestamp_updated=row.timestamp_updated,
        )
