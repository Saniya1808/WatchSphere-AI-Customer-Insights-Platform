"""
WatchSphere AI v3.0 - Global Constants
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from enum import Enum

# Project Metadata
PROJECT_NAME = "WatchSphere AI – Customer Insights Platform Version 3.0"
APP_TITLE = "WatchSphere AI"
APP_TAGLINE = "AI Powered Enterprise Customer Analytics & Business Intelligence Platform"
APP_AUTHOR = "Powered by Saniya Maner"
INTERNSHIP_CREDIT = "Infosys Internship Project 2026"

# User Roles
class UserRole(str, Enum):
    ADMIN = "admin"
    VENDOR = "vendor"
    USER = "user"


# API Routes
class APIRoutes:
    HEALTH = "/health"
    AUTH_LOGIN = "/auth/login"
    AUTH_REGISTER = "/auth/register"
    AUTH_ME = "/auth/me"
    USERS = "/users"


# Status Responses
class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    PENDING = "pending"


# Default System Tokens & UI Constants
DEFAULT_THEME = "dark"
NAV_ITEMS = [
    {"label": "Overview", "icon": "speedometer2", "key": "overview"},
    {"label": "Catalog", "icon": "grid-3x3-gap", "key": "catalog"},
    {"label": "Commerce", "icon": "cart3", "key": "commerce"},
    {"label": "Artificial Intelligence", "icon": "cpu", "key": "ai_engine"},
    {"label": "System Settings", "icon": "gear", "key": "system_settings"},
]
