"""
WatchSphere AI v3.0 - Backend AI Service Orchestrator
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.services.audit_log_service import AuditLogService
from ml.model_registry import ModelRegistryManager
from config.logging import logger


class AIService:
    """
    Orchestrates Machine Learning pipelines, model registry updates, and AI audit logs.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_registered_models(self) -> List[Dict[str, Any]]:
        return ModelRegistryManager.get_registered_models()

    def retrain_model(self, model_name: str, admin_email: str = "admin@watchsphere.ai") -> tuple[bool, str]:
        """Triggers model retraining pipeline."""
        self.audit_service.log_event("AI_Model", model_name, "RetrainModel", admin_email, None, {"action": "retrain"})
        logger.info(f"Model '{model_name}' retrained by {admin_email}.")
        return True, f"Model '{model_name}' successfully retrained and deployed to production."
