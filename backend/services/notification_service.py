"""
WatchSphere AI v3.0 - Notification & Alert Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.notification import Notification
from backend.services.audit_log_service import AuditLogService


class NotificationService:
    """
    Service dispatching in-app and email system alerts.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_all(self, status: Optional[str] = None) -> List[Notification]:
        query = self.db.query(Notification)
        if status and status != "All Statuses":
            query = query.filter(Notification.status == status)
        return query.order_by(Notification.created_at.desc()).all()

    def create_notification(self, n_data: Dict[str, Any]) -> Notification:
        notif = Notification(
            user_id=n_data.get("user_id"),
            title=n_data.get("title", "System Notification"),
            message=n_data.get("message", ""),
            category=n_data.get("category", "System"),
            channel=n_data.get("channel", "In-App"),
            status="Unread"
        )
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def mark_as_read(self, notif_id: str) -> bool:
        n = self.db.query(Notification).filter(Notification.id == notif_id).first()
        if n:
            n.status = "Read"
            self.db.commit()
            return True
        return False

    def mark_all_read(self) -> int:
        unread = self.db.query(Notification).filter(Notification.status == "Unread").all()
        count = 0
        for n in unread:
            n.status = "Read"
            count += 1
        self.db.commit()
        return count
