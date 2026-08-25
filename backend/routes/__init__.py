"""
WatchSphere AI v3.0 - Routes Package Export
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.routes.health_routes import router as health_router
from backend.routes.auth_routes import router as auth_router

__all__ = ["health_router", "auth_router"]
