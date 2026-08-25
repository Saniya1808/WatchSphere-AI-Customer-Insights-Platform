"""
WatchSphere AI v3.0 - Order Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from backend.models.base_model import BaseModel


class Order(BaseModel):
    """
    SQLAlchemy Order Model.
    """
    __tablename__ = "orders"

    order_number = Column(String(100), unique=True, index=True, nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    customer_name = Column(String(255), nullable=False)
    vendor_id = Column(String(36), ForeignKey("vendors.id"), nullable=True)
    vendor_name = Column(String(255), nullable=False)
    items_count = Column(Integer, default=1, nullable=False)

    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    gst_amount = Column(Float, default=0.0, nullable=False)
    final_amount = Column(Float, nullable=False)

    payment_method = Column(String(50), default="Credit Card", nullable=False)
    payment_status = Column(String(20), default="Paid", nullable=False)  # Pending, Paid, Failed, Refunded
    order_status = Column(String(30), default="Completed", nullable=False)  # Pending, Confirmed, Packed, Shipped, Out for Delivery, Delivered, Cancelled, Returned, Refunded

    order_date = Column(String(100), nullable=False)
    delivery_date = Column(String(100), nullable=True)
    shipping_address = Column(String(500), nullable=True)
    billing_address = Column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Order id={self.id} num='{self.order_number}' status='{self.order_status}'>"
