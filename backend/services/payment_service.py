"""
WatchSphere AI v3.0 - Payment Transaction Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from backend.models.payment import Payment
from backend.services.audit_log_service import AuditLogService


class PaymentService:
    """
    Service managing payment transactions and refund processing.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_all(self, search: Optional[str] = None, method: Optional[str] = None) -> List[Payment]:
        query = self.db.query(Payment)
        if method and method != "All Methods":
            query = query.filter(Payment.payment_method == method)
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                (Payment.transaction_id.ilike(search_term)) |
                (Payment.order_number.ilike(search_term)) |
                (Payment.customer_name.ilike(search_term))
            )
        return query.order_by(Payment.created_at.desc()).all()

    def process_refund(self, payment_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return False, "Payment record not found."

        prev_status = payment.status
        payment.status = "Refunded"
        self.db.commit()

        self.audit_service.log_event("Payment", payment.id, "Refund", admin_email, {"status": prev_status}, {"status": "Refunded"})
        return True, f"Payment '{payment.transaction_id}' refunded successfully."
