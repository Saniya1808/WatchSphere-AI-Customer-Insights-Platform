"""
WatchSphere AI v3.0 - ML Training Log Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Integer
from backend.models.base_model import BaseModel


class MLTrainingLog(BaseModel):
    """
    SQLAlchemy model recording training logs and epoch metrics.
    """
    __tablename__ = "training_logs"

    model_name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    epoch_or_step = Column(Integer, default=1, nullable=False)
    loss = Column(Float, default=0.05, nullable=False)
    metric_value = Column(Float, default=0.95, nullable=False)
    status = Column(String(50), default="Completed", nullable=False)
    logged_by = Column(String(255), default="admin@watchsphere.ai", nullable=False)
