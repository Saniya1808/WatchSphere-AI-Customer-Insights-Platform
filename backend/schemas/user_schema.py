"""
WatchSphere AI v3.0 - User Pydantic Schemas
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from config.constants import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    vendor_company: Optional[str] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    vendor_company: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
