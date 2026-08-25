"""
WatchSphere AI v3.0 - Authentication Pydantic Schemas
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from config.constants import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    vendor_company: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_role: UserRole
    full_name: str
    email: str
    vendor_company: Optional[str] = None


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    vendor_company: Optional[str] = None
