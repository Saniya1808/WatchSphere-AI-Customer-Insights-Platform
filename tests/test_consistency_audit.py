"""
WatchSphere AI v3.0 - Enterprise Consistency Audit Unit Tests
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.services.user_service import UserService
from backend.services.scheduled_report_service import ScheduledReportService
from backend.services.notification_service import NotificationService
from backend.services.api_management_service import APIManagementService
from backend.services.backup_service import BackupService


def test_user_service_complete_crud(db_session, sample_user):
    """Test UserService lock/unlock, password reset, and user deletion."""
    user_svc = UserService(db_session)
    users = user_svc.get_all_users()
    assert len(users) >= 1

    target = users[0]
    
    # Lock
    ok_l, _ = user_svc.lock_account(target.id)
    assert ok_l is True
    assert target.is_active is False

    # Unlock
    ok_u, _ = user_svc.unlock_account(target.id)
    assert ok_u is True
    assert target.is_active is True

    # Reset Password
    ok_r, _ = user_svc.reset_password(target.id, "NewPassword@123")
    assert ok_r is True

    # Roles & Permissions
    roles = user_svc.get_all_roles()
    assert len(roles) >= 4
    perms = user_svc.get_all_permissions()
    assert len(perms) >= 5


def test_scheduled_report_service_crud(db_session):
    """Test ScheduledReportService creation, run now, and deletion."""
    sched_svc = ScheduledReportService(db_session)
    ok, msg, sched = sched_svc.create_schedule({"name": "Test Audit Schedule", "frequency": "Daily", "format": "CSV"})
    assert ok is True
    assert sched.id is not None

    ok_run, _ = sched_svc.run_schedule_now(sched.id)
    assert ok_run is True

    ok_del, _ = sched_svc.delete_schedule(sched.id)
    assert ok_del is True


def test_notification_service_crud(db_session):
    """Test NotificationService creation and mark all read."""
    notif_svc = NotificationService(db_session)
    n = notif_svc.create_notification({"title": "Test Notif", "message": "Audit test", "category": "System"})
    assert n.id is not None
    assert n.status == "Unread"

    count = notif_svc.mark_all_read()
    assert count >= 1


def test_api_management_service_revoke_and_delete(db_session):
    """Test APIManagementService key generation, revocation, and deletion."""
    api_svc = APIManagementService(db_session)
    ok, msg, key_entry = api_svc.generate_api_key("Audit Test Key")
    assert ok is True
    assert key_entry.status == "Active"

    ok_rev, _ = api_svc.revoke_key(key_entry.id)
    assert ok_rev is True
    assert key_entry.status == "Revoked"

    ok_del, _ = api_svc.delete_key(key_entry.id)
    assert ok_del is True


def test_backup_service_restore(db_session):
    """Test BackupService restore point verification."""
    backup_svc = BackupService(db_session)
    ok_b, msg_b, entry = backup_svc.create_snapshot_backup()
    assert ok_b is True
    assert entry.id is not None

    ok_r, msg_r = backup_svc.restore_backup_snapshot(entry.id)
    assert ok_r is True
    assert "restored" in msg_r
