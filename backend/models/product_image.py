"""
WatchSphere AI v3.0 - Product Image Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Boolean, ForeignKey
from backend.models.base_model import BaseModel


class ProductImage(BaseModel):
    """
    SQLAlchemy Model for secondary media images attached to products.
    """
    __tablename__ = "product_images"

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_thumbnail = Column(Boolean, default=False, nullable=False)
