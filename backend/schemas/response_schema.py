"""
WatchSphere AI v3.0 - Standard API Response Wrappers
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel
from config.constants import ResponseStatus

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standardized API Envelope Response Schema.
    """
    status: ResponseStatus = ResponseStatus.SUCCESS
    message: str
    data: Optional[T] = None
    errors: Optional[Any] = None


class HealthCheckResponse(BaseModel):
    """
    System Health Status Schema.
    """
    status: str
    app_name: str
    version: str
    database_connected: bool
    timestamp: str
