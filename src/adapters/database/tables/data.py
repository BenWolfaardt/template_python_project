from uuid import uuid4  # TODO upgradet to newer version

from sqlalchemy import Column, DateTime, Index, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.adapters.database.base import DeclarativeBase


class DataRow(DeclarativeBase):
    __tablename__ = "data"
    __table_args__ = (UniqueConstraint("id"), Index("idx_id", "id"))

    id = Column(
        UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        primary_key=True,
        index=True,
    )
    data = Column(Text, nullable=False)
    timestamp_created = Column(DateTime, nullable=False)
    email = Column(DateTime, nullable=False)
