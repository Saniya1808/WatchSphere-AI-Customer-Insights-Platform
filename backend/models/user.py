"""
WatchSphere AI v3.0 - User Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Enum as SQLEnum
from config.constants import UserRole
from backend.models.base_model import BaseModel


class User(BaseModel):
    """
    SQLAlchemy User Model mapping system users, vendors, and administrators.
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    vendor_company = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)

    def __repr__(self) -> str:
        return f"<User id={self.id} email='{self.email}' role='{self.role}'>"
