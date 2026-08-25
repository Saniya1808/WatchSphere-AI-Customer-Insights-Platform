"""
WatchSphere AI v3.0 - Custom Application Exceptions
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from fastapi import HTTPException, status


class WatchSphereException(Exception):
    """Base exception class for WatchSphere AI application."""
    def __init__(self, message: str = "An unexpected enterprise platform error occurred."):
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(HTTPException):
    """Raised when authentication fails or token is invalid."""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedException(HTTPException):
    """Raised when user role lacks required permissions."""
    def __init__(self, detail: str = "Operation not permitted for current user role"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class ResourceNotFoundException(HTTPException):
    """Raised when requested entity is not found in database."""
    def __init__(self, resource: str = "Resource", identifier: str = ""):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} {identifier} was not found",
        )


class DuplicateResourceException(HTTPException):
    """Raised when unique constraint violation occurs (e.g., existing email)."""
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
