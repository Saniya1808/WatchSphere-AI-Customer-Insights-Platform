"""
WatchSphere AI v3.0 - Role & Permission Models
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String
from backend.models.base_model import BaseModel


class Role(BaseModel):
    """SQLAlchemy Role Model."""
    __tablename__ = "roles"

    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)


class Permission(BaseModel):
    """SQLAlchemy Permission Model."""
    __tablename__ = "permissions"

    module = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)  # CREATE, READ, UPDATE, DELETE, EXPORT, ADMIN
    code = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
