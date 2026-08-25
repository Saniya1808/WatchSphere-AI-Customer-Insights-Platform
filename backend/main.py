"""
WatchSphere AI v3.0 - Enterprise FastAPI Main Entry Point
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from config.settings import settings
from config.logging import logger
from config.database import engine, Base
from backend.api.router import api_router
from backend.middleware.logging_middleware import LoggingMiddleware
from backend.middleware.error_handler import global_exception_handler, validation_exception_handler


from backend.database.seed import seed_default_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan Event Handler.
    Handles startup table creation, seed user initialization, and shutdown resource cleanup.
    """
    logger.info("Initializing WatchSphere AI Backend Engine...")
    # Create DB tables automatically on startup
    Base.metadata.create_all(bind=engine)
    logger.info("Database schemas verified and synchronized.")
    
    # Trigger master dataset auto-import
    from datasets.seed_datasets import auto_seed_datasets
    auto_seed_datasets()
    seed_default_users()
    logger.info("Default seed users verified.")
    yield
    logger.info("Shutting down WatchSphere AI Backend Engine...")



# FastAPI Application Instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Powered Enterprise Customer Analytics & Business Intelligence Platform - Backend API Engine",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
app.add_middleware(LoggingMiddleware)

# Register Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include Central API Router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
