"""
WatchSphere AI v3.0 - Backup History Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float
from backend.models.base_model import BaseModel


class BackupHistory(BaseModel):
    """SQLAlchemy Backup History Model."""
    __tablename__ = "backup_history"

    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size_mb = Column(Float, nullable=False)
    backup_type = Column(String(50), default="Database Snapshot", nullable=False)
    status = Column(String(20), default="Completed", nullable=False)
    performed_by = Column(String(255), default="admin@watchsphere.ai", nullable=False)
