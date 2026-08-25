"""
WatchSphere AI v3.0 - Authentication Service Layer
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Tuple
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.services.user_service import UserService
from backend.schemas.auth_schema import LoginRequest, Token
from config.security import verify_password, create_access_token
from config.settings import settings
from backend.core.exceptions import UnauthorizedException


class AuthService:
    """
    Service layer coordinating authentication logic, credential validation, and JWT issuing.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate_user(self, login_data: LoginRequest) -> User:
        """
        Validates user credentials against stored hash.
        """
        user = self.user_service.get_by_email(login_data.email)
        if not user:
            raise UnauthorizedException("Invalid email or password")
        if not verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedException("User account is deactivated")
        return user

    def login(self, login_data: LoginRequest) -> Tuple[Token, User]:
        """
        Authenticates credentials and returns issued JWT token along with user entity.
        """
        user = self.authenticate_user(login_data)
        
        token_data = {
            "sub": user.id,
            "email": user.email,
            "role": user.role.value,
            "full_name": user.full_name,
            "vendor_company": user.vendor_company
        }
        
        access_token = create_access_token(data=token_data)
        
        token = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_role=user.role,
            full_name=user.full_name,
            email=user.email,
            vendor_company=user.vendor_company
        )
        
        return token, user
