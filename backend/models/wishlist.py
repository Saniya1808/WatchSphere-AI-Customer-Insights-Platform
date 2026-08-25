"""
WatchSphere AI v3.0 - Wishlist Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, ForeignKey
from backend.models.base_model import BaseModel


class Wishlist(BaseModel):
    """
    SQLAlchemy Wishlist Model.
    """
    __tablename__ = "wishlist"

    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    customer_name = Column(String(255), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    status = Column(String(20), default="Active", nullable=False)  # Active, Converted, Removed
