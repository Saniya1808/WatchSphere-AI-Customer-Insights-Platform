"""
WatchSphere AI v3.0 - Schemas Package Export
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.schemas.user_schema import UserBase, UserCreate, UserUpdate, UserResponse
from backend.schemas.auth_schema import LoginRequest, Token, TokenData
from backend.schemas.response_schema import APIResponse, HealthCheckResponse

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "LoginRequest",
    "Token",
    "TokenData",
    "APIResponse",
    "HealthCheckResponse",
]
