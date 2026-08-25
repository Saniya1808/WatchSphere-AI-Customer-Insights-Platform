"""
WatchSphere AI v3.0 - Scheduled Reports Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.scheduled_report_service import ScheduledReportService


def render_scheduled_reports_tab() -> None:
    """
    Renders Scheduled Reports tab connected to ScheduledReportService.
    """
    db = SessionLocal()
    try:
        sched_service = ScheduledReportService(db)
        schedules = sched_service.get_all()

        # Seed initial default schedules if DB is empty
        if not schedules:
            sched_service.create_schedule({"name": "Daily Executive Revenue Digest", "frequency": "Daily", "format": "PDF"})
            sched_service.create_schedule({"name": "Weekly Inventory Stockout Summary", "frequency": "Weekly", "format": "Excel"})
            schedules = sched_service.get_all()

        st.markdown("### ⏰ Automated Scheduled Reports Directory")

        if schedules:
            sched_rows = [{"ID": s.id[:8], "Report Name": s.name, "Frequency": s.frequency, "Format": s.format, "Delivery": s.delivery_channel, "Last Run": s.last_run or "Never", "Next Run": s.next_run or "Pending", "Status": s.status} for s in schedules]
            st.dataframe(pd.DataFrame(sched_rows), use_container_width=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                sel_rep = st.selectbox("Target Schedule", options=[s.name for s in schedules], key="sched_target_select")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("▶️ Run Schedule Now", type="primary", key="btn_exec_sched_run"):
                    target_s = next((s for s in schedules if s.name == sel_rep), None)
                    if target_s:
                        ok, msg = sched_service.run_schedule_now(target_s.id)
                        st.toast(msg)
                        st.rerun()

    finally:
        db.close()
