"""
WatchSphere AI v3.0 - Theme Manager Layout Utility
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st


class ThemeManager:
    """
    Manages frontend dark/light themes and custom token rendering.
    """

    @staticmethod
    def render_theme_toggle() -> str:
        """
        Renders theme selector control in sidebar and updates session state.
        """
        st.sidebar.markdown("### 🎨 Theme Configuration")
        current_theme = st.session_state.get("theme", "dark")
        selected_theme = st.sidebar.radio(
            "Select UI Theme",
            options=["dark", "light"],
            index=0 if current_theme == "dark" else 1,
            key="theme_radio"
        )
        st.session_state.theme = selected_theme
        return selected_theme
