"""
WatchSphere AI v3.0 - Notification Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, ForeignKey
from backend.models.base_model import BaseModel


class Notification(BaseModel):
    """SQLAlchemy Notification Model."""
    __tablename__ = "notifications"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    category = Column(String(50), default="System", nullable=False)  # System, Inventory, Payment, Forecast, Security
    channel = Column(String(50), default="In-App", nullable=False)   # In-App, Email
    status = Column(String(20), default="Unread", nullable=False)     # Unread, Read, Archived
