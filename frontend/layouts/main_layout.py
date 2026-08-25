"""
WatchSphere AI v3.0 - Main Structural Layout Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.components.header import render_header
from frontend.components.footer import render_footer
from frontend.layouts.navigation import NavigationManager
from frontend.layouts.theme import ThemeManager
from frontend.utils.css_loader import load_css


def apply_main_layout():
    """
    Applies the full enterprise layout shell:
    - CSS styling load
    - Header component
    - Sidebar navigation & Theme configuration
    - Returns active selected navigation section
    """
    # Load custom CSS
    load_css()

    # Render top header
    render_header()

    # Sidebar layout controls
    active_section = NavigationManager.render_sidebar_menu()
    st.sidebar.markdown("---")
    ThemeManager.render_theme_toggle()

    return active_section
