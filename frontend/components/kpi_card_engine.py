"""
WatchSphere AI v3.0 - 12-KPI Card Engine Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any
import streamlit as st


def render_kpi_engine_grid(kpis: Dict[str, Dict[str, Any]]) -> None:
    """
    Renders 12 reusable executive KPI cards in a 4-column responsive grid.
    """
    st.markdown("### 📈 Executive Key Performance Indicators")

    kpi_keys = list(kpis.keys())
    for row_idx in range(0, len(kpi_keys), 4):
        cols = st.columns(4)
        for col_idx in range(4):
            if row_idx + col_idx < len(kpi_keys):
                key = kpi_keys[row_idx + col_idx]
                kpi = kpis[key]
                col = cols[col_idx]
                
                trend_color = "#10B981" if kpi["trend"] == "up" else ("#F43F5E" if kpi["trend"] == "down" else "#94A3B8")
                trend_icon = "▲" if kpi["trend"] == "up" else ("▼" if kpi["trend"] == "down" else "•")

                with col:
                    st.markdown(
                        f"""
                        <div class="ws-glass-card" style="padding: 20px; position: relative;" title="{kpi['tooltip']}">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.4rem;">{kpi['icon']}</span>
                                <span style="font-size: 0.75rem; font-weight: 700; color: {trend_color}; background: rgba(16, 185, 129, 0.1); padding: 3px 8px; border-radius: 9999px;">
                                    {trend_icon} {kpi['change']}
                                </span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--text-sub); text-transform: uppercase; font-weight: 600; margin-top: 10px;">
                                {kpi['title']}
                            </div>
                            <div style="font-size: 1.6rem; font-weight: 800; color: var(--text-main); margin: 6px 0;">
                                {kpi['value']}
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: var(--text-muted);">
                                <span>MoM: {kpi['prev_val']}</span>
                                <span style="color: var(--accent-indigo); font-weight: 600;">Sparkline: ▅▆▇█</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
