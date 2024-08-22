from collections.abc import Generator
from contextlib import contextmanager
from uuid import UUID

from psycopg2 import errors
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.adapters.database.tables.data import DataRow
from src.adapters.logger import Logger
from src.core.models.data import Data
from src.core.models.exceptions import DataAlreadyExists, DataEmpty, DataIDNotFound
from src.core.ports.store import Store


UniqueViolation = errors.lookup("23505")


# TODO: all methods should be async? Does this require SQLAlchemy 2.0?
class SQLStore(Store):
    def __init__(self, connection_url: str, logger: Logger) -> None:
        self.engine = create_engine(connection_url)
        self.session = sessionmaker(self.engine)
        self.logger = logger
        self.exceptions = logger.Exceptions(logger)

    def create(self, data: Data) -> Data:
        with self.write_session() as session:
            try:
                row_insert = self._data_to_data_row(data)
                session.add(row_insert)
                session.flush()

                self.logger.info(f"ID {row_insert.id} successfully written to Data DB.")

            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    self.logger.warning(
                        f"ID {row_insert.id} already exists in Data DB.",
                    )
                    raise DataAlreadyExists(row_insert.id) from e
                else:
                    self.logger.exception(f"ID {row_insert.id} unsuccessfully written to Data DB.")
                    raise

            else:
                return data

    def read(self, id: UUID) -> Data:
        with self.read_session() as session:
            try:
                row = session.query(DataRow).filter_by(id=id).first()
                if not row:
                    raise DataIDNotFound(id)

                self.logger.info(
                    f"ID {id} successfully read from Data DB.",
                )
                return self._data_row_to_data(row)

            except DataIDNotFound:
                self.logger.warning(
                    f"ID {id} not found in Data DB.",
                )
                raise

            except Exception as e:
                self.exceptions.log_exception(
                    f"An unexpected error occurred whilst trying to read id {id} from Data DB.",
                    e,
                )
                raise

    def read_all(self, id: UUID | None) -> list[Data]:
        with self.read_session() as session:
            try:
                query_params = {
                    "id": id,
                }
                query = session.query(DataRow)

                if id:
                    query = query.filter(DataRow.id == id)

                rows = query.all()
                if not rows:
                    raise DataEmpty(**query_params)

                datas = [self._data_row_to_data(row) for row in rows]
                ids = [data.id for data in datas]
                self.logger.info(
                    f"IDs {ids} successfully read from Data DB matching query params: {query_params}.",
                )

            except DataEmpty:
                self.logger.warning(
                    f"No data exists in the Data DB matching query params: {query_params}.",
                )
                raise

            except Exception as e:
                self.exceptions.log_exception(
                    f"An unexpected error occurred whilst trying to read data from Data DB. Query params: {query_params}.",
                    e,
                )
                raise

            else:
                return datas

    def update(self, data: Data) -> Data:
        with self.write_session() as session:
            try:
                row = session.query(DataRow).filter_by(id=data.id).first()

                if not row:
                    raise DataIDNotFound(data.id)

                row_update = self._data_to_data_row(data)

                session.merge(row_update)
                session.flush()

                self.logger.info(
                    f"ID {data.id} successfully updated in Data DB.",
                )

            except DataIDNotFound:
                self.logger.warning(
                    f"ID {data.id} unsuccessfully updated as user not found in Data DB.",
                )
                raise

            except Exception as e:
                self.exceptions.log_exception(
                    f"An unexpected error occurred whilst trying to updater ID {data.id}, in the Data DB.",
                    e,
                )
                raise

            else:
                return data

    def delete(self, id: UUID) -> bool:
        with self.write_session() as session:
            try:
                row = session.query(DataRow).filter_by(id=id).first()

                if not row:
                    raise DataIDNotFound(id)

                session.delete(row)
                self.logger.info(
                    f"ID {id} successfully deleted from Data DB.",
                )

            except DataIDNotFound:
                self.logger.warning(f"ID {id} not found when trying to delete user from Data DB.")
                return False

            except Exception as e:
                self.exceptions.log_exception(f"Failed to delete ID {id} from Data DB.", e)
                return False

            else:
                return True

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
        data: Data,
    ) -> DataRow:
        return DataRow(**data.__dict__)

    @staticmethod
    def _data_row_to_data(row: DataRow) -> Data:
        return Data(**row.__dict__)
