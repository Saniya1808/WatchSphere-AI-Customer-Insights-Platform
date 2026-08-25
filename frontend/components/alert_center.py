"""
WatchSphere AI v3.0 - Real-Time Executive Alert Center
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Dict, Any
import streamlit as st


def render_alert_center(alerts: List[Dict[str, Any]]) -> None:
    """
    Renders 8 Executive Real-Time Bento Alert Cards.
    """
    st.markdown("### 🚨 Executive Real-Time Alert Center")

    cols = st.columns(4)
    for idx, alert in enumerate(alerts):
        col = cols[idx % 4]
        with col:
            st.markdown(
                f"""
                <div class="ws-glass-card" style="padding: 16px; border-left: 4px solid {alert['color']}; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.75rem; font-weight: 700; color: {alert['color']}; text-transform: uppercase;">
                            {alert['priority']} PRIORITY
                        </span>
                        <span style="font-size: 0.75rem; color: var(--text-muted);">{alert['timestamp']}</span>
                    </div>
                    <h4 style="margin: 8px 0 4px 0; font-size: 1rem; color: var(--text-main);">{alert['title']}</h4>
                    <p style="font-size: 0.8rem; color: var(--text-sub); margin: 0 0 12px 0; line-height: 1.4;">
                        {alert['description']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"⚡ {alert['action']}", key=f"btn_alert_{alert['id']}", use_container_width=True):
                st.toast(f"Triggered action: {alert['action']}", icon="⚡")
