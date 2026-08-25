"""
WatchSphere AI v3.0 - Category Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Integer, Float
from backend.models.base_model import BaseModel


class Category(BaseModel):
    """
    SQLAlchemy Category Model mapping main catalog product categories.
    """
    __tablename__ = "categories"

    name = Column(String(255), unique=True, index=True, nullable=False)
    image_url = Column(String(500), nullable=True)
    description = Column(String(1000), nullable=True)
    display_order = Column(Integer, default=1, nullable=False)
    status = Column(String(20), default="Active", nullable=False)  # Active, Hidden
    products_count = Column(Integer, default=0, nullable=False)
    revenue = Column(Float, default=0.0, nullable=False)

    def __repr__(self) -> str:
        return f"<Category id={self.id} name='{self.name}'>"
