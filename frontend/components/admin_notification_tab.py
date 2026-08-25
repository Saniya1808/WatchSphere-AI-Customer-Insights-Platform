"""
WatchSphere AI v3.0 - Notification Center Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.notification_service import NotificationService


def render_notification_tab() -> None:
    """
    Renders Notification Center tab connected to NotificationService.
    """
    db = SessionLocal()
    try:
        notif_service = NotificationService(db)
        notifications = notif_service.get_all()

        # Seed initial default notifications if empty
        if not notifications:
            notif_service.create_notification({"title": "Admin Login Detected", "message": "Successful login from IP 127.0.0.1", "category": "Security"})
            notif_service.create_notification({"title": "Low Stock Warning", "message": "SKU-002 reached 4 units remaining", "category": "Inventory"})
            notifications = notif_service.get_all()

        st.markdown("### 🔔 System Alerts & Notification Center")

        if notifications:
            n_rows = [{"ID": n.id[:8], "Category": n.category, "Title": n.title, "Message": n.message, "Status": n.status, "Channel": n.channel, "Timestamp": n.created_at} for n in notifications]
            st.dataframe(pd.DataFrame(n_rows), use_container_width=True)

            if st.button("Mark All Alerts as Read", type="primary", key="btn_mark_all_notifs"):
                count = notif_service.mark_all_read()
                st.toast(f"Marked {count} alerts as read.")
                st.rerun()

    finally:
        db.close()
