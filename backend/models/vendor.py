"""
WatchSphere AI v3.0 - Vendor Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Integer
from backend.models.base_model import BaseModel


class Vendor(BaseModel):
    """
    SQLAlchemy Vendor Entity Model mapping onboarded enterprise suppliers.
    """
    __tablename__ = "vendors"

    company_name = Column(String(255), nullable=False)
    logo_url = Column(String(500), nullable=True)
    owner_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=False)
    gst_number = Column(String(100), unique=True, index=True, nullable=False)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    status = Column(String(20), default="Active", nullable=False)  # Active, Suspended
    products_count = Column(Integer, default=0, nullable=False)
    revenue = Column(Float, default=0.0, nullable=False)
    rating = Column(Float, default=4.8, nullable=False)
    last_login = Column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<Vendor id={self.id} company='{self.company_name}' email='{self.email}'>"
