"""
WatchSphere AI v3.0 - Order Processing Repository Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.order import Order
from backend.services.audit_log_service import AuditLogService
from config.logging import logger


class OrderService:
    """
    CRUD Repository pattern service for Order entities with status workflow management.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all(
        self,
        search: Optional[str] = None,
        vendor_name: Optional[str] = None,
        order_status: Optional[str] = None
    ) -> List[Order]:
        """
        Retrieves orders with optional vendor scoping and status filtering.
        If vendor_name is provided, filters strictly for that vendor's orders.
        """
        query = self.db.query(Order)
        if vendor_name and vendor_name != "All Vendors":
            query = query.filter(Order.vendor_name == vendor_name)
        if order_status and order_status != "All Statuses":
            query = query.filter(Order.order_status == order_status)
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                (Order.order_number.ilike(search_term)) |
                (Order.customer_name.ilike(search_term)) |
                (Order.vendor_name.ilike(search_term))
            )
        return query.order_by(Order.created_at.desc()).all()

    def update_order_status(self, order_id: str, new_status: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Updates order status along workflow pipeline."""
        order = self.get_by_id(order_id)
        if not order:
            return False, "Order not found."

        prev = order.order_status
        order.order_status = new_status
        if new_status == "Refunded":
            order.payment_status = "Refunded"

        self.db.commit()
        self.audit_service.log_event("Order", order.id, f"UpdateOrderStatus_{new_status}", admin_email, {"status": prev}, {"status": new_status})
        return True, f"Order #{order.order_number} status updated to '{new_status}'."
