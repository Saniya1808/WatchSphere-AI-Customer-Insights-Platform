"""
WatchSphere AI v3.0 - Review & Rating Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, ForeignKey
from backend.models.base_model import BaseModel


class Review(BaseModel):
    """
    SQLAlchemy Review & Rating Model.
    """
    __tablename__ = "reviews"

    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    customer_name = Column(String(255), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    vendor_id = Column(String(36), ForeignKey("vendors.id"), nullable=True)
    vendor_name = Column(String(255), nullable=False)

    rating = Column(Float, nullable=False)
    title = Column(String(255), nullable=False)
    review_text = Column(String(2000), nullable=False)
    sentiment = Column(String(20), default="Positive", nullable=False)  # Positive, Neutral, Negative
    status = Column(String(20), default="Approved", nullable=False)    # Approved, Pending Moderation, Rejected, Hidden

    def __repr__(self) -> str:
        return f"<Review id={self.id} prod='{self.product_name}' rating={self.rating}>"
