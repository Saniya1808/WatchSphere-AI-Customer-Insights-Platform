"""
WatchSphere AI v3.0 - Customer Repository Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.customer import Customer
from backend.services.audit_log_service import AuditLogService
from config.logging import logger


class CustomerService:
    """
    CRUD Repository pattern service for Customer entities.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.email == email.lower().strip()).first()

    def get_all(self, search: Optional[str] = None, segment: Optional[str] = None) -> List[Customer]:
        query = self.db.query(Customer)
        if segment and segment != "All Segments":
            query = query.filter(Customer.segment == segment)
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                (Customer.full_name.ilike(search_term)) |
                (Customer.email.ilike(search_term)) |
                (Customer.city.ilike(search_term))
            )
        return query.order_by(Customer.created_at.desc()).all()

    def update_status(self, customer_id: str, new_status: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        customer = self.get_by_id(customer_id)
        if not customer:
            return False, "Customer not found."

        prev = customer.status
        customer.status = new_status
        self.db.commit()

        self.audit_service.log_event("Customer", customer.id, f"SetStatus_{new_status}", admin_email, {"status": prev}, {"status": new_status})
        return True, f"Customer status updated to '{new_status}'."
