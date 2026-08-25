"""
WatchSphere AI v3.0 - Enterprise Header Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from config.constants import PROJECT_NAME, APP_TAGLINE, APP_AUTHOR, INTERNSHIP_CREDIT


def render_header() -> None:
    """
    Renders the platform enterprise top banner with branding, versioning, author attribution, and status indicators.
    """
    st.markdown(
        f"""
        <div class="ws-header">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h1 class="ws-title-gradient" style="margin: 0; font-size: 2.2rem; line-height: 1.2;">{PROJECT_NAME}</h1>
                    <p style="color: #94A3B8; margin: 4px 0 0 0; font-size: 1rem; font-weight: 400;">{APP_TAGLINE}</p>
                </div>
                <div style="text-align: right; margin-top: 10px;">
                    <span class="ws-badge ws-badge-active"><span class="status-dot"></span>System Operational</span>
                    <span class="ws-badge ws-badge-brand">Phase 1 Foundation</span>
                    <div style="margin-top: 6px; font-size: 0.85rem; color: #818CF8; font-weight: 600;">
                        {APP_AUTHOR} | {INTERNSHIP_CREDIT}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
