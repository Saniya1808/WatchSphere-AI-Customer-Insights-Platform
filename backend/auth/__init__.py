"""
WatchSphere AI v3.0 - Auth Package Export
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.auth.dependencies import get_current_user, require_role, oauth2_scheme
from backend.auth.jwt import create_access_token, decode_access_token
from backend.auth.password import hash_password, verify_password

__all__ = [
    "get_current_user",
    "require_role",
    "oauth2_scheme",
    "create_access_token",
    "decode_access_token",
    "hash_password",
    "verify_password",
]
