"""
WatchSphere AI v3.0 - Database & Model Unit Tests (Phase 2)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.models.user import User
from backend.services.user_service import UserService
from backend.schemas.user_schema import UserCreate
from config.constants import UserRole


def test_create_vendor_user(db_session):
    """Test vendor user creation with company name via repository service."""
    user_service = UserService(db_session)
    user_in = UserCreate(
        email="vendor.test@watchsphere.ai",
        password="SecureVendorPassword123!",
        full_name="Acme Rep",
        vendor_company="Acme Corp",
        role=UserRole.VENDOR
    )
    user = user_service.create(user_in)
    
    assert user.id is not None
    assert user.email == "vendor.test@watchsphere.ai"
    assert user.role == UserRole.VENDOR
    assert user.vendor_company == "Acme Corp"
    assert user.hashed_password != "SecureVendorPassword123!"


def test_get_by_email(db_session, sample_user):
    """Test retrieving user by email address."""
    user_service = UserService(db_session)
    found_user = user_service.get_by_email(sample_user.email)
    
    assert found_user is not None
    assert found_user.id == sample_user.id
    assert found_user.full_name == sample_user.full_name
