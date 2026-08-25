"""
WatchSphere AI v3.0 - Audit Logging Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.models.audit_log import AuditLog
from config.logging import logger


class AuditLogService:
    """
    Service recording Admin mutation events for compliance and security auditing.
    """

    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        entity_name: str,
        entity_id: str,
        action: str,
        admin_email: str,
        previous_val: Optional[Dict[str, Any]] = None,
        new_val: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Records an audit log entry into database."""
        try:
            log_entry = AuditLog(
                entity_name=entity_name,
                entity_id=str(entity_id),
                action=action,
                admin_email=admin_email,
                previous_value=json.dumps(previous_val) if previous_val else None,
                new_value=json.dumps(new_val) if new_val else None
            )
            self.db.add(log_entry)
            self.db.commit()
            self.db.refresh(log_entry)
            logger.info(f"Audit Log recorded: {action} on {entity_name}:{entity_id} by {admin_email}")
            return log_entry
        except Exception as e:
            logger.error(f"Failed to record audit log: {str(e)}")
            self.db.rollback()
            return None

    def get_logs_for_entity(self, entity_name: str, entity_id: str) -> List[AuditLog]:
        """Retrieves history logs for specific entity."""
        return self.db.query(AuditLog).filter(
            AuditLog.entity_name == entity_name,
            AuditLog.entity_id == str(entity_id)
        ).order_by(AuditLog.created_at.desc()).all()

    def get_recent_logs(self, limit: int = 50) -> List[AuditLog]:
        """Retrieves recent global audit logs."""
        return self.db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
