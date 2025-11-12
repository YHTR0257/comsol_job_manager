"""Base SQLAlchemy model for the ESP project."""

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class TimestampMixin:
    """Mixin for adding timestamp fields to models."""

    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False
    )