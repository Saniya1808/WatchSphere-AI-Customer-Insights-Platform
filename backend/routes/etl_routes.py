"""
WatchSphere AI v3.0 - ETL Pipeline & Dataset Management API Routes
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.services.dataset_manager import DatasetManager
from backend.services.etl_pipeline_service import ETLPipelineService

router = APIRouter(prefix="/etl", tags=["ETL & Dataset Ingestion Engine"])


@router.get("/status", summary="Get Status of All CSV Datasets")
def get_datasets_status():
    """
    Returns status metadata for all 22 expected WatchSphere CSV datasets.
    """
    statuses = DatasetManager.get_all_dataset_status()
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved status metadata for {len(statuses)} datasets",
        data=statuses
    )


@router.post("/upload", summary="Upload & Ingest Multi-Format Dataset")
async def upload_dataset(
    file: UploadFile = File(...),
    import_mode: str = Form("Append"),
    db: Session = Depends(get_db)
):
    """
    Processes uploaded dataset file (CSV, XLSX, JSON, Parquet, TSV, ZIP) with schema auto-detection and data quality scoring.
    """
    try:
        content = await file.read()
        etl_service = ETLPipelineService(db)
        ok, msg, quality = etl_service.process_file_upload(
            file_bytes=content,
            filename=file.filename,
            import_mode=import_mode
        )
        if not ok:
            raise HTTPException(status_code=400, detail=msg)
            
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message=msg,
            data={
                "filename": file.filename,
                "detected_schema": quality.get("detected_schema"),
                "total_rows": quality.get("total_rows"),
                "quality_score_pct": quality.get("quality_score_pct")
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ETL upload error: {str(e)}")
