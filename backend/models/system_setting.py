"""
WatchSphere AI v3.0 - System Setting Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Text
from backend.models.base_model import BaseModel


class SystemSetting(BaseModel):
    """SQLAlchemy System Setting Model."""
    __tablename__ = "system_settings"

    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
    category = Column(String(50), default="General", nullable=False)  # General, Tax, Security, Email
    description = Column(String(255), nullable=True)
