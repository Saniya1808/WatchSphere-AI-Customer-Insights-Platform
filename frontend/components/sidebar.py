"""
WatchSphere AI v3.0 - Enterprise Collapsible Sidebar Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.utils.session import SessionManager
from config.constants import APP_AUTHOR, INTERNSHIP_CREDIT

try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False


def render_sidebar() -> str:
    """
    Renders collapsible enterprise sidebar with logo, navigation menu clusters, user profile badge, and logout option.
    Returns: Selected page title ('Overview', 'Catalog', 'Commerce', 'Artificial Intelligence', 'System Settings')
    """
    user_email = SessionManager.get_user_email() or "admin@watchsphere.ai"
    user_role = (SessionManager.get_user_role() or "admin").upper()

    with st.sidebar:
        # Logo & Brand Header
        st.markdown(
            """
            <div style="padding: 10px 0 16px 0; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #6366F1, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    ⚡ WatchSphere AI
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px;">
                    Enterprise Analytics Platform
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        menu_items = ["Overview", "Catalog", "Commerce", "Artificial Intelligence", "System Settings", "Logout"]
        menu_icons = ["speedometer2", "grid-3x3-gap-fill", "cart-fill", "cpu", "gear-wide-connected", "box-arrow-right"]

        current_page = st.session_state.get("current_page", "Overview")
        default_idx = menu_items.index(current_page) if current_page in menu_items else 0

        if HAS_OPTION_MENU:
            selected = option_menu(
                menu_title=None,
                options=menu_items,
                icons=menu_icons,
                default_index=default_idx,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#6366F1", "font-size": "16px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "6px 0",
                        "padding": "10px 14px",
                        "border-radius": "12px",
                        "--hover-color": "rgba(99, 102, 241, 0.15)",
                        "font-weight": "500"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #6366F1, #4F46E5)",
                        "color": "#FFFFFF",
                        "font-weight": "700",
                        "box-shadow": "0 4px 12px rgba(99, 102, 241, 0.35)"
                    },
                }
            )
        else:
            selected = st.radio("Navigation", options=menu_items)

        # Handle Logout selection
        if selected == "Logout":
            SessionManager.clear_session()
            st.rerun()

        st.session_state.current_page = selected

        # User Profile & Role Footer
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="padding: 12px; background: rgba(15, 23, 42, 0.6); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 12px;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Logged In User</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{user_email}</div>
                <div style="margin-top: 6px;">
                    <span class="ws-badge ws-badge-brand" style="font-size: 0.7rem;">ROLE: {user_role}</span>
                </div>
            </div>
            <div style="padding: 10px; background: rgba(99, 102, 241, 0.08); border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2); text-align: center; font-size: 0.75rem;">
                <div style="font-weight: 700; color: #6366F1;">{APP_AUTHOR}</div>
                <div style="color: #94A3B8; margin-top: 2px;">{INTERNSHIP_CREDIT}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        return selected
