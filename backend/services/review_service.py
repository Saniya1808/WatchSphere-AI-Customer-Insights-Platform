"""
WatchSphere AI v3.0 - Review & Rating Moderation Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from backend.models.review import Review
from backend.services.audit_log_service import AuditLogService


class ReviewService:
    """
    Review moderation service with sentiment tagging (Positive, Neutral, Negative).
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_all(self, vendor_name: Optional[str] = None, sentiment: Optional[str] = None) -> List[Review]:
        query = self.db.query(Review)
        if vendor_name and vendor_name != "All Vendors":
            query = query.filter(Review.vendor_name == vendor_name)
        if sentiment and sentiment != "All Sentiments":
            query = query.filter(Review.sentiment == sentiment)
        return query.order_by(Review.created_at.desc()).all()

    def moderate_review(self, review_id: str, action: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Approve, Reject, Hide, Delete review."""
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return False, "Review not found."

        if action == "Delete":
            self.db.delete(review)
            self.audit_service.log_event("Review", review_id, "Delete", admin_email, {"title": review.title}, None)
        else:
            prev = review.status
            review.status = "Approved" if action == "Approve" else ("Rejected" if action == "Reject" else "Hidden")
            self.audit_service.log_event("Review", review_id, f"Moderate_{action}", admin_email, {"status": prev}, {"status": review.status})

        self.db.commit()
        return True, f"Review moderation '{action}' executed."
