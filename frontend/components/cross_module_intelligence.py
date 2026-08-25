"""
WatchSphere AI v3.0 - Cross-Module Executive Intelligence Cards
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any
import streamlit as st


def render_cross_module_intelligence(intel_data: Dict[str, Dict[str, Any]]) -> None:
    """
    Renders 4 Cross-Module Intelligence Bento Cards.
    """
    st.markdown("### 🧠 Cross-Module Executive Intelligence")

    cols = st.columns(4)
    modules = [
        ("customer_intel", "👥", "#6366F1"),
        ("product_intel", "⌚", "#8B5CF6"),
        ("payment_intel", "💳", "#10B981"),
        ("inventory_intel", "🏭", "#0EA5E9")
    ]

    for idx, (key, icon, accent) in enumerate(modules):
        col = cols[idx]
        item = intel_data[key]
        with col:
            st.markdown(
                f"""
                <div class="ws-glass-card" style="padding: 20px; border-top: 4px solid {accent}; height: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.5rem;">{icon}</span>
                        <span style="font-size: 0.75rem; font-weight: 700; color: {accent}; background: rgba(99, 102, 241, 0.1); padding: 3px 8px; border-radius: 9999px;">
                            {item['trend']}
                        </span>
                    </div>
                    <h4 style="margin: 12px 0 6px 0; font-size: 1.1rem; color: var(--text-main);">{item['title']}</h4>
                    <div style="display: flex; gap: 12px; font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 8px;">
                        <span>• {item['kpi_1']}</span>
                        <span>• {item['kpi_2']}</span>
                    </div>
                    <p style="font-size: 0.8rem; color: var(--text-sub); margin-bottom: 14px; line-height: 1.5;">
                        {item['summary']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"🔍 {item['action']}", key=f"btn_intel_{key}", use_container_width=True):
                st.toast(f"Navigating to {item['title']} detail...", icon="🔍")
