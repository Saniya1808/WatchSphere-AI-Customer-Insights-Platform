"""
WatchSphere AI v3.0 - Order Item Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from backend.models.base_model import BaseModel


class OrderItem(BaseModel):
    """
    SQLAlchemy OrderItem Model.
    """
    __tablename__ = "order_items"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    subtotal = Column(Float, nullable=False)
