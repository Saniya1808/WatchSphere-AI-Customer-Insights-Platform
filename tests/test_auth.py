"""
WatchSphere AI v3.0 - Authentication & Security Unit Tests
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from config.security import hash_password, verify_password, create_access_token, decode_access_token
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import LoginRequest


def test_password_hashing():
    """Verify bcrypt password hashing and verification."""
    password = "MySuperSecretPassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_generation_and_decoding():
    """Verify JWT token encoding and decoding."""
    payload = {"sub": "user-12345", "role": "admin"}
    token = create_access_token(data=payload)
    
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded.get("sub") == "user-12345"
    assert decoded.get("role") == "admin"


def test_auth_service_login(db_session, sample_user):
    """Test successful user login authentication via AuthService."""
    auth_service = AuthService(db_session)
    login_req = LoginRequest(
        email="testuser@watchsphere.ai",
        password="TestPassword123!"
    )
    
    token, user = auth_service.login(login_req)
    assert token.access_token is not None
    assert token.user_role == sample_user.role
    assert user.id == sample_user.id
