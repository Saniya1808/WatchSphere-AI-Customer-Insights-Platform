"""
WatchSphere AI v3.0 - Scheduled Report Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String
from backend.models.base_model import BaseModel


class ScheduledReport(BaseModel):
    """SQLAlchemy ScheduledReport Model."""
    __tablename__ = "scheduled_reports"

    name = Column(String(255), nullable=False)
    report_type = Column(String(100), nullable=False)  # Sales, Revenue, Customer, Inventory, AI Forecast
    frequency = Column(String(50), default="Weekly", nullable=False)  # Daily, Weekly, Monthly, Quarterly, Yearly
    format = Column(String(20), default="PDF", nullable=False)        # PDF, Excel, CSV, HTML
    delivery_channel = Column(String(50), default="Email", nullable=False)  # Email, Local Storage, Cloud Storage
    recipient_email = Column(String(255), nullable=False)
    last_run = Column(String(100), nullable=True)
    next_run = Column(String(100), nullable=True)
    status = Column(String(20), default="Active", nullable=False)     # Active, Disabled
