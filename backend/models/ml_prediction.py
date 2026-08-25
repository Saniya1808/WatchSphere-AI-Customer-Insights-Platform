"""
WatchSphere AI v3.0 - ML Prediction Cache Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Text
from backend.models.base_model import BaseModel


class MLPrediction(BaseModel):
    """
    SQLAlchemy model caching generated AI predictions.
    """
    __tablename__ = "predictions"

    model_name = Column(String(255), nullable=False)
    target_entity_id = Column(String(255), nullable=True)
    input_data = Column(Text, nullable=True)
    prediction_output = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.95, nullable=False)
