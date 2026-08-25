"""
WatchSphere AI v3.0 - Enterprise Footer Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from config.constants import APP_AUTHOR, INTERNSHIP_CREDIT


def render_footer() -> None:
    """
    Renders standard copyright and metadata footer.
    """
    st.markdown(
        f"""
        <div class="ws-footer">
            <p style="margin: 0;">
                © 2026 <strong>WatchSphere AI Platform v3.0</strong>. All Rights Reserved.
            </p>
            <p style="margin: 4px 0 0 0; color: #64748B;">
                {APP_AUTHOR} • {INTERNSHIP_CREDIT} • Production Architecture Phase 1
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
