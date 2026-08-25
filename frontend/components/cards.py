"""
WatchSphere AI v3.0 - Reusable UI Card Components
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st


def render_metric_card(title: str, value: str, subtitle: str = "", badge_text: str = "") -> None:
    """
    Renders a glassmorphism metric summary card.
    """
    badge_html = f'<span class="ws-badge ws-badge-brand" style="float: right;">{badge_text}</span>' if badge_text else ""
    st.markdown(
        f"""
        <div class="ws-card">
            {badge_html}
            <div style="font-size: 0.875rem; color: #94A3B8; font-weight: 500; text-transform: uppercase;">{title}</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #F8FAFC; margin: 8px 0;">{value}</div>
            <div style="font-size: 0.8rem; color: #38BDF8;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_architecture_card(layer_name: str, tech_stack: str, description: str, status: str = "Active") -> None:
    """
    Renders an architectural layer summary card.
    """
    st.markdown(
        f"""
        <div class="ws-card">
            <span class="ws-badge ws-badge-active" style="float: right;">{status}</span>
            <h3 style="margin: 0 0 8px 0; color: #38BDF8; font-size: 1.2rem;">{layer_name}</h3>
            <p style="margin: 0 0 12px 0; font-weight: 600; color: #CBD5E1; font-size: 0.9rem;">Stack: {tech_stack}</p>
            <p style="margin: 0; color: #94A3B8; font-size: 0.875rem; line-height: 1.5;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
