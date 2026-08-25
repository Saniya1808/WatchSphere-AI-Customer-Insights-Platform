"""
WatchSphere AI v3.0 - Configuration Module
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from config.settings import settings
from config.constants import (
    APP_TITLE,
    APP_TAGLINE,
    APP_AUTHOR,
    PROJECT_NAME,
    UserRole,
)
from config.logging import logger
from config.database import Base, engine, SessionLocal, get_db

__all__ = [
    "settings",
    "APP_TITLE",
    "APP_TAGLINE",
    "APP_AUTHOR",
    "PROJECT_NAME",
    "UserRole",
    "logger",
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
]
