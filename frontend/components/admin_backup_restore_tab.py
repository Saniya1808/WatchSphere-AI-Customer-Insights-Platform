"""
WatchSphere AI v3.0 - Backup & Restore Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.backup_service import BackupService


def render_backup_restore_tab() -> None:
    """
    Renders Backup & Restore tab with live BackupService wiring and snapshot recovery.
    """
    db = SessionLocal()
    try:
        backup_service = BackupService(db)
        history = backup_service.get_backup_history()

        st.markdown("### 💾 Database Backup & Snapshot Governance")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("💡 Full database snapshot backs up all SQLite database tables into an encrypted `.db` recovery file.")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⚡ Create Snapshot Backup", type="primary", key="btn_exec_create_backup"):
                ok, msg, _ = backup_service.create_snapshot_backup()
                st.success(msg)
                st.rerun()

        st.markdown("#### 📜 Backup Recovery Points History")
        if history:
            h_rows = [{"ID": h.id[:8], "File": h.file_name, "Size (MB)": f"{h.file_size_mb:.1f}", "Type": h.backup_type, "Status": h.status, "Performed By": h.performed_by, "Timestamp": h.created_at} for h in history]
            st.dataframe(pd.DataFrame(h_rows), use_container_width=True)

            col_b, col_r = st.columns([3, 1])
            with col_b:
                sel_b_id = st.selectbox("Select Target Snapshot to Restore", options=[h.id for h in history], key="backup_restore_select")
            with col_r:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Restore Snapshot", type="primary", key="btn_exec_restore_backup"):
                    if sel_b_id:
                        ok, msg = backup_service.restore_backup_snapshot(sel_b_id)
                        st.success(msg)
                        st.rerun()
        else:
            st.info("No backup snapshots created yet.")

    finally:
        db.close()
