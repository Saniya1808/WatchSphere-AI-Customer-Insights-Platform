"""
WatchSphere AI v3.0 - Global Exception Handler Middleware
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config.logging import logger
from config.constants import ResponseStatus


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global catch-all exception handler converting uncaught exceptions into clean JSON responses.
    """
    logger.error(f"Global exception caught on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": ResponseStatus.ERROR.value,
            "message": "An internal enterprise platform error occurred.",
            "data": None,
            "errors": [str(exc)] if True else None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler for Pydantic schema validation failures.
    """
    logger.warning(f"Validation error on {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": ResponseStatus.ERROR.value,
            "message": "Input validation error.",
            "data": None,
            "errors": exc.errors()
        }
    )
