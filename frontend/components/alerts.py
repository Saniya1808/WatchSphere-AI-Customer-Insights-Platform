"""
WatchSphere AI v3.0 - Reusable Alert Notifications
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st


def render_alert(message: str, alert_type: str = "info") -> None:
    """
    Renders standard alert banners (success, warning, error, info).
    """
    if alert_type == "success":
        st.success(message)
    elif alert_type == "warning":
        st.warning(message)
    elif alert_type == "error":
        st.error(message)
    else:
        st.info(message)
