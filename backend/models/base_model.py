"""
WatchSphere AI v3.0 - Abstract Base Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from config.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseModel(Base):
    """
    Abstract SQLAlchemy Base Model providing common audit columns:
    - Primary Key (UUID String)
    - Created At Timestamp
    - Updated At Timestamp
    - Active Status Flag
    """
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
