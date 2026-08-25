"""
WatchSphere AI v3.0 - Scheduled Report Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models.scheduled_report import ScheduledReport
from backend.services.audit_log_service import AuditLogService
from config.logging import logger


class ScheduledReportService:
    """
    CRUD repository & execution service for automated scheduled reports.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_by_id(self, report_id: str) -> Optional[ScheduledReport]:
        return self.db.query(ScheduledReport).filter(ScheduledReport.id == report_id).first()

    def get_all(self, status: Optional[str] = None) -> List[ScheduledReport]:
        query = self.db.query(ScheduledReport)
        if status and status != "All Statuses":
            query = query.filter(ScheduledReport.status == status)
        return query.order_by(ScheduledReport.created_at.desc()).all()

    def create_schedule(self, s_data: Dict[str, Any], admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, Optional[ScheduledReport]]:
        """Creates a new automated report schedule."""
        try:
            schedule = ScheduledReport(
                name=s_data.get("name"),
                report_type=s_data.get("report_type", "Sales Report"),
                frequency=s_data.get("frequency", "Weekly"),
                format=s_data.get("format", "PDF"),
                delivery_channel=s_data.get("delivery_channel", "Email"),
                recipient_email=s_data.get("recipient_email", admin_email),
                last_run="Never",
                next_run=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M"),
                status=s_data.get("status", "Active")
            )
            self.db.add(schedule)
            self.db.commit()
            self.db.refresh(schedule)

            self.audit_service.log_event("ScheduledReport", schedule.id, "CreateSchedule", admin_email, None, s_data)
            return True, f"Report schedule '{schedule.name}' created successfully.", schedule
        except Exception as e:
            self.db.rollback()
            return False, f"Failed to create schedule: {str(e)}", None

    def run_schedule_now(self, schedule_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Manually triggers immediate execution of a report schedule."""
        schedule = self.get_by_id(schedule_id)
        if not schedule:
            return False, "Schedule not found."

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        schedule.last_run = now_str
        self.db.commit()

        self.audit_service.log_event("ScheduledReport", schedule.id, "RunScheduleNow", admin_email, None, {"run_at": now_str})
        return True, f"Schedule '{schedule.name}' executed manually! Report dispatched to {schedule.recipient_email}."

    def delete_schedule(self, schedule_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Deletes a report schedule."""
        schedule = self.get_by_id(schedule_id)
        if not schedule:
            return False, "Schedule not found."

        self.db.delete(schedule)
        self.db.commit()

        self.audit_service.log_event("ScheduledReport", schedule_id, "DeleteSchedule", admin_email, {"name": schedule.name}, None)
        return True, f"Schedule '{schedule.name}' deleted."
