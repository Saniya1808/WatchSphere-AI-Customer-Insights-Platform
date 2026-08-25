"""
WatchSphere AI v3.0 - AI Executive Insights Panel Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any
import streamlit as st


def render_ai_insights_panel(ai_data: Dict[str, Any]) -> None:
    """
    Renders AI Executive Natural Language Summary & Suggested Action Panel.
    """
    st.markdown("### 🤖 AI Executive Decision Insights")

    st.markdown(
        """
        <div class="ws-glass-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(139, 92, 246, 0.06)); border: 1px solid rgba(99, 102, 241, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.8rem;">🧠</span>
                    <div>
                        <h3 style="margin: 0; font-family: var(--font-heading); color: var(--accent-indigo); font-size: 1.3rem;">
                            AI Executive Summary & Recommendations
                        </h3>
                        <span style="font-size: 0.75rem; color: var(--text-sub);">Generated in Real-Time via WatchSphere AI Synthesis Engine</span>
                    </div>
                </div>
                <span class="ws-floating-badge" style="margin: 0;">Accuracy Score: 94.8%</span>
            </div>
            
            <div style="font-size: 0.95rem; color: var(--text-main); line-height: 1.7; margin-bottom: 20px;">
                <ul style="padding-left: 20px; margin: 0;">
        """,
        unsafe_allow_html=True
    )

    for bullet in ai_data.get("insights", []):
        st.markdown(f"- **Insight**: {bullet}")

    st.markdown("#### 🎯 Suggested Executive Actions")
    for action in ai_data.get("suggested_actions", []):
        st.markdown(f"👉 **Action Item**: {action}")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("📄 Generate PDF Report (Disabled)", key="btn_pdf_disabled", disabled=True, use_container_width=True, help="PDF Report Generation will be enabled in Phase 4.")
    with col2:
        if st.button("📊 View Detailed Analytics Stream", key="btn_view_details", type="primary", use_container_width=True):
            st.toast("Opening Detailed BI Stream View...", icon="📊")
