"""
WatchSphere AI v3.0 - Modular Database Configuration
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from config.settings import settings
from config.logging import logger

# SQLite specific connect args; ignored seamlessly for PostgreSQL/MySQL
engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

# SQLAlchemy 2.0 Engine Creation
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    **engine_kwargs
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Declarative Base Model
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI & Application Dependency that provides a database session context per request.
    Ensures session cleanup on completion or exception.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def check_db_connection() -> bool:
    """
    Health check function to verify database connectivity.
    """
    try:
        with engine.connect() as connection:
            logger.info("Database connectivity check successful.")
            return True
    except Exception as e:
        logger.error(f"Database connection health check failed: {str(e)}")
        return False
