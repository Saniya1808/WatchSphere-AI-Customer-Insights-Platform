"""
WatchSphere AI v3.0 - Enterprise Administration Suite Unit Tests (Phase 7)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.services.reporting_service import ReportingService
from backend.services.notification_service import NotificationService
from backend.services.backup_service import BackupService
from backend.services.permission_service import PermissionService
from backend.services.monitoring_service import MonitoringService
from backend.services.api_management_service import APIManagementService


def test_reporting_service():
    """Test Multi-Domain Report Generation."""
    data = [{"Metric": "Revenue", "Value": 15000}]
    pdf_bytes, filename = ReportingService.generate_report_bytes("Sales Report", "PDF", data)
    assert len(pdf_bytes) > 0
    assert "sales_report.pdf" == filename

    excel_bytes, ex_filename = ReportingService.generate_report_bytes("Inventory Report", "Excel", data)
    assert len(excel_bytes) > 0
    assert "inventory_report.xlsx" == ex_filename


def test_backup_service(db_session):
    """Test Snapshot Backup generation."""
    backup_svc = BackupService(db_session)
    ok, msg, entry = backup_svc.create_snapshot_backup("admin@watchsphere.ai")
    assert ok is True
    assert entry.file_name.startswith("watchsphere_backup_")


def test_permission_service():
    """Test RBAC Permission Matrix."""
    matrix = PermissionService.get_permission_matrix()
    assert "Admin" in matrix
    assert matrix["Admin"]["System Backup"] is True
    assert matrix["Vendor"]["User Management"] is False


def test_monitoring_service():
    """Test System Telemetry Health Collector."""
    health = MonitoringService.get_system_health()
    assert health["database_status"] == "HEALTHY"
    assert health["cpu_usage_pct"] > 0


def test_api_management_service(db_session):
    """Test API Key Generation."""
    api_svc = APIManagementService(db_session)
    ok, msg, key_entry = api_svc.generate_api_key("Partner API")
    assert ok is True
    assert key_entry.api_key_hash.startswith("ws_live_")
