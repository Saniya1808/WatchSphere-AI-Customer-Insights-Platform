"""
WatchSphere AI v3.0 - API Key Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Integer
from backend.models.base_model import BaseModel


class APIKey(BaseModel):
    """SQLAlchemy API Key Model."""
    __tablename__ = "api_keys"

    key_name = Column(String(255), nullable=False)
    api_key_hash = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(String(36), nullable=False)
    user_email = Column(String(255), nullable=False)
    rate_limit_per_min = Column(Integer, default=100, nullable=False)
    status = Column(String(20), default="Active", nullable=False)  # Active, Revoked
    expires_at = Column(String(100), nullable=True)
