"""
WatchSphere AI v3.0 - Customer Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Integer
from backend.models.base_model import BaseModel


class Customer(BaseModel):
    """
    SQLAlchemy Customer Model mapping platform shoppers and enterprise accounts.
    """
    __tablename__ = "customers"

    photo_url = Column(String(500), nullable=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), unique=True, index=True, nullable=False)
    gender = Column(String(20), default="Unspecified", nullable=False)
    age = Column(Integer, default=30, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    segment = Column(String(50), default="Regular Consumer", nullable=False)  # Enterprise VIP, Regular Consumer, High Net Worth, Corporate Account
    status = Column(String(20), default="Active", nullable=False)  # Active, Inactive
    orders_count = Column(Integer, default=0, nullable=False)
    total_spending = Column(Float, default=0.0, nullable=False)
    avg_order_value = Column(Float, default=0.0, nullable=False)
    last_purchase_date = Column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<Customer id={self.id} name='{self.full_name}' email='{self.email}'>"
