"""
WatchSphere AI v3.0 - Payment Transaction Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, ForeignKey
from backend.models.base_model import BaseModel


class Payment(BaseModel):
    """
    SQLAlchemy Payment Transaction Model.
    """
    __tablename__ = "payments"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    order_number = Column(String(100), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    customer_name = Column(String(255), nullable=False)

    payment_method = Column(String(50), nullable=False)  # UPI, Credit Card, Debit Card, Net Banking, COD, Wallet
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    gateway = Column(String(50), default="Stripe / Razorpay", nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="Paid", nullable=False)  # Pending, Paid, Failed, Refunded
    payment_date = Column(String(100), nullable=False)
