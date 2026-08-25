"""
WatchSphere AI v3.0 - User Service Repository Layer
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user_schema import UserCreate, UserUpdate
from backend.services.audit_log_service import AuditLogService
from config.security import hash_password
from backend.core.exceptions import DuplicateResourceException, ResourceNotFoundException
from config.logging import logger


class UserService:
    """
    Repository pattern service handling database operations for User entities.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Fetch user by primary key ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch user by unique email address."""
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def create(self, user_in: UserCreate) -> User:
        """
        Creates a new user record after verifying email uniqueness and hashing password.
        """
        existing_user = self.get_by_email(user_in.email)
        if existing_user:
            raise DuplicateResourceException(f"User with email '{user_in.email}' already exists.")

        db_user = User(
            email=user_in.email.lower().strip(),
            hashed_password=hash_password(user_in.password),
            full_name=user_in.full_name,
            vendor_company=user_in.vendor_company,
            role=user_in.role,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        self.audit_service.log_event("User", db_user.id, "CreateUser", "admin@watchsphere.ai", None, {"email": db_user.email, "role": db_user.role})
        return db_user

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieve paginated list of users."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_all_users(self) -> List[User]:
        """Alias for get_all() returning all user accounts."""
        return self.get_all()

    def update(self, user_id: str, user_in: UserUpdate) -> User:
        """Update existing user attributes."""
        user = self.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        update_data = user_in.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"]:
            update_data["email"] = update_data["email"].lower().strip()

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def lock_account(self, user_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Locks a user account (sets is_active=False)."""
        user = self.get_by_id(user_id)
        if not user:
            return False, "User not found."

        user.is_active = False
        self.db.commit()

        self.audit_service.log_event("User", user.id, "LockAccount", admin_email, {"is_active": True}, {"is_active": False})
        return True, f"User account '{user.email}' locked successfully."

    def unlock_account(self, user_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Unlocks a user account (sets is_active=True)."""
        user = self.get_by_id(user_id)
        if not user:
            return False, "User not found."

        user.is_active = True
        self.db.commit()

        self.audit_service.log_event("User", user.id, "UnlockAccount", admin_email, {"is_active": False}, {"is_active": True})
        return True, f"User account '{user.email}' unlocked successfully."

    def reset_password(self, user_id: str, new_pwd: str = "Reset@123", admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Resets user password."""
        user = self.get_by_id(user_id)
        if not user:
            return False, "User not found."

        user.hashed_password = hash_password(new_pwd)
        self.db.commit()

        self.audit_service.log_event("User", user.id, "ResetPassword", admin_email, None, {"action": "reset_password"})
        return True, f"Password for '{user.email}' reset successfully."

    def delete_user(self, user_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Deletes user account."""
        user = self.get_by_id(user_id)
        if not user:
            return False, "User not found."

        self.db.delete(user)
        self.db.commit()

        self.audit_service.log_event("User", user_id, "DeleteUser", admin_email, {"email": user.email}, None)
        return True, f"User '{user.email}' deleted successfully."

    def get_all_roles(self) -> List[Dict[str, str]]:
        """Returns standard enterprise roles."""
        return [
            {"code": "ADMIN", "name": "Administrator", "description": "Full System Access"},
            {"code": "VENDOR", "name": "Vendor Partner", "description": "Scoped Product & Order Access"},
            {"code": "MANAGER", "name": "Enterprise Manager", "description": "Reporting & Catalog Management"},
            {"code": "ANALYST", "name": "Data Analyst", "description": "Read-Only BI & AI Insights"},
            {"code": "SUPPORT", "name": "Customer Support", "description": "Order & Review Support"}
        ]

    def get_all_permissions(self) -> List[Dict[str, str]]:
        """Returns list of system permissions."""
        return [
            {"module": "Catalog", "action": "READ"},
            {"module": "Catalog", "action": "WRITE"},
            {"module": "Commerce", "action": "READ"},
            {"module": "Commerce", "action": "WRITE"},
            {"module": "AI Engine", "action": "READ"},
            {"module": "AI Engine", "action": "ADMIN"},
            {"module": "System Admin", "action": "ADMIN"}
        ]
