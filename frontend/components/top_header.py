"""
WatchSphere AI v3.0 - Sticky Top Header Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime, timezone
import streamlit as st
from frontend.utils.session import SessionManager


def render_top_header() -> None:
    """
    Renders the sticky enterprise header containing:
    - Search Box
    - Notifications Icon
    - Animated Sun/Moon Theme Switcher
    - Current User Profile Avatar & Badge
    - Date & Time Live Display
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%A, %b %d, %Y")
    time_str = now.strftime("%H:%M UTC")

    user_name = SessionManager.get_user_name()
    user_role = (SessionManager.get_user_role() or "user").upper()
    initials = "".join([part[0] for part in user_name.split()[:2]]).upper()

    current_theme = st.session_state.get("theme", "dark")
    theme_icon = "🌙 Dark" if current_theme == "dark" else "☀️ Light"

    col_search, col_actions, col_profile = st.columns([2.5, 2, 2.5])

    with col_search:
        st.text_input("🔍 Search Platform...", key="header_search", label_visibility="collapsed", placeholder="🔍 Search insights, catalog...")

    with col_actions:
        col_theme, col_notif = st.columns([1.5, 1])
        with col_theme:
            if st.button(f"{theme_icon}", key="top_theme_toggle", help="Toggle Light / Dark Mode"):
                st.session_state.theme = "light" if current_theme == "dark" else "dark"
                st.rerun()
        with col_notif:
            st.button("🔔 3", key="top_notifications", help="3 System Notifications")

    with col_profile:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; align-items: center; gap: 12px;">
                <div style="text-align: right; line-height: 1.2;">
                    <div style="font-weight: 700; font-size: 0.9rem; color: var(--text-main);">{user_name}</div>
                    <div style="font-size: 0.75rem; color: var(--accent-indigo); font-weight: 600;">{user_role} • {date_str} {time_str}</div>
                </div>
                <div class="ws-avatar">{initials}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<hr style='margin: 10px 0 20px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
