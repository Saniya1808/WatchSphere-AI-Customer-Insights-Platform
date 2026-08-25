"""
WatchSphere AI v3.0 - ML Model Registry Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float
from backend.models.base_model import BaseModel


class MLModel(BaseModel):
    """
    SQLAlchemy model representing registered Machine Learning models.
    """
    __tablename__ = "ml_models"

    name = Column(String(255), unique=True, index=True, nullable=False)
    version = Column(String(50), nullable=False)
    algorithm = Column(String(100), nullable=False)
    task_type = Column(String(100), nullable=False)  # Classification, Regression, Clustering, Recommendation, NLP, Anomaly
    accuracy = Column(Float, default=0.95, nullable=False)
    precision = Column(Float, default=0.94, nullable=False)
    recall = Column(Float, default=0.93, nullable=False)
    f1_score = Column(Float, default=0.94, nullable=False)
    roc_auc = Column(Float, default=0.96, nullable=False)
    status = Column(String(20), default="Active", nullable=False)  # Active, Retraining, Inactive
    last_trained_at = Column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<MLModel id={self.id} name='{self.name}' v='{self.version}' acc={self.accuracy}>"
