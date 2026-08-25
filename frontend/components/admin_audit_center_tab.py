"""
WatchSphere AI v3.0 - Audit Center Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.audit_log_service import AuditLogService
from backend.services.catalog_export_service import CatalogExportService


def render_audit_center_tab() -> None:
    """
    Renders Audit Center tab with global event history timeline and CSV download.
    """
    db = SessionLocal()
    try:
        audit_service = AuditLogService(db)
        logs = audit_service.get_recent_logs(50)

        st.markdown("### 📜 Global System Audit Trail & Security Timeline")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("🔍 Search Audit Events...", key="audit_search_input", placeholder="Entity, Action, Admin email...")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            export_btn = st.button("📥 Export Audit Logs", key="btn_export_audit_logs", use_container_width=True)

        if logs:
            l_rows = [{"ID": l.id[:8], "Entity": l.entity_name, "Action": l.action, "Admin": l.admin_email, "Prev State": l.previous_value or "N/A", "New State": l.new_value or "N/A", "Timestamp": l.created_at} for l in logs]
            df_logs = pd.DataFrame(l_rows)
            st.dataframe(df_logs, use_container_width=True)

            if export_btn:
                csv_data = CatalogExportService.export_to_csv(l_rows)
                st.download_button("Download Audit Logs CSV", data=csv_data, file_name="audit_logs_export.csv", mime="text/csv")
        else:
            st.info("No audit events recorded.")

    finally:
        db.close()
