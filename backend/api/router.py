"""
WatchSphere AI v3.0 - Central API Router
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from fastapi import APIRouter
from backend.routes.health_routes import router as health_router
from backend.routes.auth_routes import router as auth_router
from backend.routes.catalog_routes import router as catalog_router
from backend.routes.commerce_routes import router as commerce_router
from backend.routes.dashboard_routes import router as dashboard_router
from backend.routes.analytics_routes import router as analytics_router
from backend.routes.ai_routes import router as ai_router
from backend.routes.reporting_routes import router as reporting_router
from backend.routes.etl_routes import router as etl_router

api_router = APIRouter()

# Register sub-routers under /api/v1
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(catalog_router)
api_router.include_router(commerce_router)
api_router.include_router(dashboard_router)
api_router.include_router(analytics_router)
api_router.include_router(ai_router)
api_router.include_router(reporting_router)
api_router.include_router(etl_router)

