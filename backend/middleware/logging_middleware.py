"""
WatchSphere AI v3.0 - HTTP Request Logging Middleware
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware recording incoming HTTP requests, response status codes, and execution duration.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path
        method = request.method
        client_host = request.client.host if request.client else "unknown"

        logger.info(f"Incoming Request: {method} {path} from {client_host}")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"Completed Response: {method} {path} -> Status {response.status_code} ({process_time:.2f}ms)"
            )
            response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
            return response
        except Exception as exc:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"Unhandled Request Error: {method} {path} failed ({process_time:.2f}ms) - {str(exc)}")
            raise exc
