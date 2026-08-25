"""
WatchSphere AI v3.0 - Inventory Transaction Audit Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from backend.models.base_model import BaseModel


class InventoryTransaction(BaseModel):
    """
    SQLAlchemy Inventory Transaction Model recording Stock In, Stock Out, Adjust, Transfer actions.
    """
    __tablename__ = "inventory_transactions"

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False)
    warehouse = Column(String(100), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # Stock In, Stock Out, Adjust Stock, Warehouse Transfer
    quantity = Column(Integer, nullable=False)
    previous_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)
    performed_by = Column(String(255), default="admin@watchsphere.ai", nullable=False)
