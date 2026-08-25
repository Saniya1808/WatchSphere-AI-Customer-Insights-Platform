"""
WatchSphere AI v3.0 - API Management & Token Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import uuid
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from backend.models.api_key import APIKey
from backend.services.audit_log_service import AuditLogService


class APIManagementService:
    """
    Manages API keys, rate limits, and access tokens.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def generate_api_key(self, key_name: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, APIKey]:
        raw_key = f"ws_live_{uuid.uuid4().hex}"
        key_entry = APIKey(
            key_name=key_name,
            api_key_hash=raw_key,
            user_id="admin-001",
            user_email=admin_email,
            rate_limit_per_min=100,
            status="Active"
        )
        self.db.add(key_entry)
        self.db.commit()
        self.db.refresh(key_entry)

        self.audit_service.log_event("APIKey", key_entry.id, "GenerateKey", admin_email, None, {"name": key_name})
        return True, f"API Key '{key_name}' generated successfully.", key_entry

    def get_keys(self) -> List[APIKey]:
        return self.db.query(APIKey).order_by(APIKey.created_at.desc()).all()

    def revoke_key(self, key_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        key = self.db.query(APIKey).filter(APIKey.id == key_id).first()
        if not key:
            return False, "API Key not found."

        prev = key.status
        key.status = "Revoked"
        self.db.commit()

        self.audit_service.log_event("APIKey", key.id, "RevokeKey", admin_email, {"status": prev}, {"status": "Revoked"})
        return True, f"API Key '{key.key_name}' revoked successfully."

    def delete_key(self, key_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        key = self.db.query(APIKey).filter(APIKey.id == key_id).first()
        if not key:
            return False, "API Key not found."

        self.db.delete(key)
        self.db.commit()

        self.audit_service.log_event("APIKey", key_id, "DeleteKey", admin_email, {"name": key.key_name}, None)
        return True, f"API Key '{key.key_name}' deleted."
