"""
WatchSphere AI v3.0 - Session State Manager (Phase 2)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
import streamlit as st
from config.constants import DEFAULT_THEME


class SessionManager:
    """
    Encapsulated manager for reading, writing, and enforcing Streamlit session state properties.
    """

    @staticmethod
    def initialize_session() -> None:
        """Initializes default state keys if not present."""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user" not in st.session_state:
            st.session_state.user = None
        if "token" not in st.session_state:
            st.session_state.token = None
        if "last_login" not in st.session_state:
            st.session_state.last_login = None
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Overview"
        if "theme" not in st.session_state:
            st.session_state.theme = DEFAULT_THEME
        if "sidebar_collapsed" not in st.session_state:
            st.session_state.sidebar_collapsed = False

    @staticmethod
    def set_user_session(user_dict: Dict[str, Any], token: str) -> None:
        """Stores authenticated user profile, timestamps, and JWT token into session."""
        st.session_state.authenticated = True
        st.session_state.user = user_dict
        st.session_state.token = token
        st.session_state.last_login = datetime.now(timezone.utc).strftime("%b %d, %Y - %H:%M:%S UTC")
        st.session_state.current_page = "Overview"

    @staticmethod
    def clear_session() -> None:
        """Clears user session state (logout)."""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.last_login = None
        st.session_state.current_page = "Overview"

    @staticmethod
    def is_authenticated() -> bool:
        """Returns True if user is currently logged in."""
        return st.session_state.get("authenticated", False)

    @staticmethod
    def get_user_role() -> Optional[str]:
        """Returns active user role ('admin' or 'vendor')."""
        user = st.session_state.get("user")
        return user.get("role") if user else None

    @staticmethod
    def get_user_name() -> str:
        """Returns active user's full name."""
        user = st.session_state.get("user")
        return user.get("full_name", "User") if user else "User"

    @staticmethod
    def get_user_email() -> str:
        """Returns active user's email."""
        user = st.session_state.get("user")
        return user.get("email", "") if user else ""

    @staticmethod
    def get_last_login() -> str:
        """Returns stored last login timestamp."""
        return st.session_state.get("last_login", "Just Now")

    @staticmethod
    def get_token() -> Optional[str]:
        """Returns stored JWT token."""
        return st.session_state.get("token", None)
