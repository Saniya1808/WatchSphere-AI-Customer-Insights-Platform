"""
WatchSphere AI v3.0 - Navigation Manager
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from config.constants import NAV_ITEMS

try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False


class NavigationManager:
    """
    Renders top or sidebar navigation menu using streamlit-option-menu.
    """

    @staticmethod
    def render_sidebar_menu() -> str:
        """
        Renders enterprise navigation menu in sidebar and returns current active menu selection.
        """
        st.sidebar.markdown("### 🧭 Navigation Engine")
        
        menu_titles = [item["title"] for item in NAV_ITEMS]
        menu_icons = [item["icon"] for item in NAV_ITEMS]

        if HAS_OPTION_MENU:
            selected = option_menu(
                menu_title=None,
                options=menu_titles,
                icons=menu_icons,
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#38BDF8", "font-size": "16px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "4px",
                        "border-radius": "8px",
                        "--hover-color": "rgba(56, 189, 248, 0.15)",
                    },
                    "nav-link-selected": {"background-color": "#1E293B", "color": "#38BDF8", "font-weight": "600"},
                }
            )
        else:
            selected = st.sidebar.radio("Navigation", options=menu_titles)

        st.session_state.current_nav = selected
        return selected
