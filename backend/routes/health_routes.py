"""
WatchSphere AI v3.0 - Health Check API Routes
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.settings import settings
from config.constants import APIRoutes, ResponseStatus
from config.database import get_db, check_db_connection
from backend.schemas.response_schema import APIResponse, HealthCheckResponse

router = APIRouter(tags=["Health & System"])


@router.get(
    APIRoutes.HEALTH,
    response_model=APIResponse[HealthCheckResponse],
    status_code=status.HTTP_200_OK,
    summary="System Health Check"
)
def system_health_check(db: Session = Depends(get_db)):
    """
    Returns platform vitality, versioning metadata, and database connection status.
    """
    db_ok = check_db_connection()
    health_data = HealthCheckResponse(
        status="healthy" if db_ok else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        database_connected=db_ok,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="WatchSphere AI platform status operational",
        data=health_data
    )
