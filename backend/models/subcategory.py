"""
WatchSphere AI v3.0 - Subcategory Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from backend.models.base_model import BaseModel


class Subcategory(BaseModel):
    """
    SQLAlchemy Subcategory Model mapping sub-level catalog divisions.
    """
    __tablename__ = "subcategories"

    name = Column(String(255), index=True, nullable=False)
    parent_category_id = Column(String(36), ForeignKey("categories.id"), nullable=False)
    parent_category_name = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=True)
    description = Column(String(1000), nullable=True)
    status = Column(String(20), default="Active", nullable=False)  # Active, Hidden
    products_count = Column(Integer, default=0, nullable=False)
    revenue = Column(Float, default=0.0, nullable=False)

    def __repr__(self) -> str:
        return f"<Subcategory id={self.id} name='{self.name}' parent='{self.parent_category_name}'>"
