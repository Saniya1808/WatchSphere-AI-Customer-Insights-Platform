"""
WatchSphere AI v3.0 - Database Seeding Utility
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from config.logging import logger
from config.constants import UserRole
from config.security import hash_password
from backend.models.user import User


def seed_default_users(db: Session = None) -> None:
    """
    Seeds initial default Admin and Vendor accounts into SQLite DB if they do not exist.
    """
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # 1. Seed Admin User
        admin_email = "admin@watchsphere.ai"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                email=admin_email,
                hashed_password=hash_password("Admin@123"),
                full_name="System Administrator",
                vendor_company=None,
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            logger.info(f"Seeded default Admin user: {admin_email}")

        # 2. Seed Vendor User
        vendor_email = "vendor@watchsphere.ai"
        vendor_user = db.query(User).filter(User.email == vendor_email).first()
        if not vendor_user:
            vendor_user = User(
                email=vendor_email,
                hashed_password=hash_password("Vendor@123"),
                full_name="Acme Watch Co. Representative",
                vendor_company="Acme Watch Co.",
                role=UserRole.VENDOR,
                is_active=True
            )
            db.add(vendor_user)
            logger.info(f"Seeded default Vendor user: {vendor_email}")

        db.commit()
    except Exception as e:
        logger.error(f"Error seeding database users: {str(e)}")
        db.rollback()
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_default_users()
