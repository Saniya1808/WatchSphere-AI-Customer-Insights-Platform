"""
WatchSphere AI v3.0 - Pytest Fixtures
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base
from backend.services.user_service import UserService
from backend.schemas.user_schema import UserCreate
from config.constants import UserRole

# In-memory SQLite for isolated test suite execution
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh in-memory database schema for each test function.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user(db_session):
    """
    Creates a sample user fixture in the test database.
    """
    user_service = UserService(db_session)
    user_in = UserCreate(
        email="testuser@watchsphere.ai",
        password="TestPassword123!",
        full_name="Saniya Maner Test",
        role=UserRole.ADMIN
    )
    return user_service.create(user_in)
