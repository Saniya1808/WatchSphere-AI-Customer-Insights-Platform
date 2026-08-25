"""
WatchSphere AI v3.0 - Customer Address Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Boolean, ForeignKey
from backend.models.base_model import BaseModel


class CustomerAddress(BaseModel):
    """
    SQLAlchemy Customer Address Model.
    """
    __tablename__ = "customer_addresses"

    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    address_type = Column(String(50), default="Shipping", nullable=False)  # Shipping, Billing
    street = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
