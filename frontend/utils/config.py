"""
WatchSphere AI v3.0 - Streamlit Page Configuration Utility
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from config.constants import APP_TITLE, APP_TAGLINE


def init_page_config() -> None:
    """
    Sets global Streamlit page configuration, title, layout, and icon.
    """
    st.set_page_config(
        page_title=f"{APP_TITLE} | Enterprise Insights",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
