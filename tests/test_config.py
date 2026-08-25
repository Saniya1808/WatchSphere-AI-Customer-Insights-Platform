"""
WatchSphere AI v3.0 - Configuration Unit Tests
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from config.settings import settings
from config.constants import PROJECT_NAME, APP_AUTHOR, UserRole


def test_settings_load():
    """Verify system settings load default metadata properly."""
    assert settings.APP_NAME is not None
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.ALGORITHM == "HS256"


def test_constants():
    """Verify application constants and user roles."""
    assert "WatchSphere AI" in PROJECT_NAME
    assert "Saniya Maner" in APP_AUTHOR
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.VENDOR.value == "vendor"
    assert UserRole.USER.value == "user"
