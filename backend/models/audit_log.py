"""
WatchSphere AI v3.0 - Audit Log Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Text
from backend.models.base_model import BaseModel


class AuditLog(BaseModel):
    """
    SQLAlchemy Audit Log model recording all Admin mutation events.
    """
    __tablename__ = "audit_logs"

    entity_name = Column(String(100), nullable=False)  # Vendor, Category, Subcategory, Product
    entity_id = Column(String(36), nullable=False)
    action = Column(String(50), nullable=False)        # Create, Update, Delete, Suspend, Activate
    admin_email = Column(String(255), nullable=False)
    previous_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<AuditLog id={self.id} entity='{self.entity_name}' action='{self.action}' by='{self.admin_email}'>"
