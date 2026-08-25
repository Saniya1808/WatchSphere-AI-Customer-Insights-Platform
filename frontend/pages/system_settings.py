"""
WatchSphere AI v3.0 - Enterprise Administration & Governance Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.utils.session import SessionManager
from frontend.components.footer import render_footer
from frontend.components.dataset_upload_studio import render_dataset_upload_studio
from frontend.components.admin_reports_center_tab import render_reports_center_tab
from frontend.components.admin_scheduled_reports_tab import render_scheduled_reports_tab
from frontend.components.admin_user_role_tab import render_user_role_tab
from frontend.components.admin_permission_tab import render_permission_tab
from frontend.components.admin_audit_center_tab import render_audit_center_tab
from frontend.components.admin_notification_tab import render_notification_tab
from frontend.components.admin_backup_restore_tab import render_backup_restore_tab
from frontend.components.admin_settings_tab import render_settings_tab
from frontend.components.admin_api_management_tab import render_api_management_tab
from frontend.components.admin_monitoring_tab import render_monitoring_tab


def render_system_settings_page() -> None:
    """
    Renders the complete Enterprise Administration & Governance Suite with 11 Tabs:
    1. Dataset Manager (ETL Studio)
    2. Reports Center
    3. Scheduled Reports
    4. User & Role Management
    5. Permission Management
    6. Audit Center
    7. Notification Center
    8. Backup & Restore
    9. System Settings
    10. API Management
    11. Monitoring Dashboard
    """
    user_role = (SessionManager.get_user_role() or "").lower()

    if user_role not in ["admin", "manager"]:
        st.markdown(
            """
            <div class="ws-glass-card" style="border-left: 5px solid #F43F5E; padding: 40px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 12px;">🚫</div>
                <h2 style="font-family: var(--font-heading); color: #F43F5E; margin: 0 0 10px 0;">
                    Access Restricted — Administration Suite
                </h2>
                <p style="color: var(--text-sub); max-width: 500px; margin: 0 auto 16px auto; font-size: 1rem;">
                    The Enterprise Administration Suite is restricted exclusively to Administrator and Management accounts.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        render_footer()
        return

    st.markdown(
        f"""
        <div class="ws-breadcrumb">
            Home / <span>Enterprise Administration</span>
        </div>
        <div style="margin-bottom: 16px;">
            <h1 style="font-family: var(--font-heading); font-size: 2.2rem; margin: 0; color: var(--text-main);">
                Enterprise Administration Suite
            </h1>
            <p style="color: var(--accent-indigo); font-size: 1rem; font-weight: 600; margin: 4px 0 0 0;">
                Dataset Manager, User Governance, Security RBAC & System Configuration
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tabs = st.tabs([
        "📤 1. Dataset Manager",
        "📄 2. Reports Center",
        "⏰ 3. Scheduled Reports",
        "👤 4. User Management",
        "🔐 5. Permission RBAC",
        "📜 6. Audit Center",
        "🔔 7. Notification Center",
        "💾 8. Backup & Restore",
        "⚙️ 9. System Settings",
        "🔑 10. API Management",
        "🖥️ 11. System Monitoring"
    ])

    with tabs[0]:
        render_dataset_upload_studio()
    with tabs[1]:
        render_reports_center_tab()
    with tabs[2]:
        render_scheduled_reports_tab()
    with tabs[3]:
        render_user_role_tab()
    with tabs[4]:
        render_permission_tab()
    with tabs[5]:
        render_audit_center_tab()
    with tabs[6]:
        render_notification_tab()
    with tabs[7]:
        render_backup_restore_tab()
    with tabs[8]:
        render_settings_tab()
    with tabs[9]:
        render_api_management_tab()
    with tabs[10]:
        render_monitoring_tab()

    render_footer()
