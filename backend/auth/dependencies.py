"""
WatchSphere AI v3.0 - Security & Role Authentication Dependencies
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Callable, List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.database import get_db
from config.security import decode_access_token
from config.constants import UserRole
from backend.models.user import User
from backend.services.user_service import UserService
from backend.core.exceptions import UnauthorizedException, PermissionDeniedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency validating current bearer JWT token and returning database User entity.
    """
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Invalid authentication token or token expired")

    user_id: str = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload structure")

    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise UnauthorizedException("User associated with token does not exist")
    if not user.is_active:
        raise UnauthorizedException("User account is inactive")

    return user


def require_role(allowed_roles: List[UserRole]) -> Callable:
    """
    Role-Based Access Control (RBAC) dependency factory enforcing role requirements.
    Example: Depends(require_role([UserRole.ADMIN, UserRole.VENDOR]))
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise PermissionDeniedException(
                f"Role '{current_user.role.value}' is not authorized. Allowed roles: {[r.value for r in allowed_roles]}"
            )
        return current_user

    return role_checker
