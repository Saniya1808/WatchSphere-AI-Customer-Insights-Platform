"""
WatchSphere AI v3.0 - Services Package Export
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.services.user_service import UserService
from backend.services.auth_service import AuthService

__all__ = ["UserService", "AuthService"]
