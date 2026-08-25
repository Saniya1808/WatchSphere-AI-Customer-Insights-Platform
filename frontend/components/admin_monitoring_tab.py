"""
WatchSphere AI v3.0 - Monitoring Dashboard Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.graph_objects as go
from backend.services.monitoring_service import MonitoringService
from frontend.components.cards import render_metric_card


def render_monitoring_tab() -> None:
    """
    Renders Monitoring Dashboard tab with live CPU, Memory, Disk gauges and DB connection pool telemetry.
    """
    health = MonitoringService.get_system_health()

    st.markdown("### 🖥️ Real-Time System Health & Telemetry Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("CPU Load", f"{health['cpu_usage_pct']}%", "4 Cores Active", "Active")
    with c2:
        render_metric_card("Memory Usage", f"{health['memory_usage_pct']}%", "3.4 GB / 8 GB", "VIP")
    with c3:
        render_metric_card("Disk Space", f"{health['disk_usage_pct']}%", "31.8 GB Used", "Catalog")
    with c4:
        render_metric_card("API Latency", f"{health['api_response_time_ms']} ms", "P99 Latency Mean", "Success")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        fig_cpu = go.Figure(go.Indicator(mode="gauge+number", value=health['cpu_usage_pct'], title={'text': "CPU Usage (%)"}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#6366F1"}}))
        fig_cpu.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"}, height=240)
        st.plotly_chart(fig_cpu, use_container_width=True)

    with col2:
        fig_mem = go.Figure(go.Indicator(mode="gauge+number", value=health['memory_usage_pct'], title={'text': "Memory Usage (%)"}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#8B5CF6"}}))
        fig_mem.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"}, height=240)
        st.plotly_chart(fig_mem, use_container_width=True)

    with col3:
        fig_disk = go.Figure(go.Indicator(mode="gauge+number", value=health['disk_usage_pct'], title={'text': "Disk Usage (%)"}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#10B981"}}))
        fig_disk.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"}, height=240)
        st.plotly_chart(fig_disk, use_container_width=True)

    st.markdown(
        f"""
        <div class="ws-glass-card" style="padding: 20px; margin-top: 15px;">
            <h4>🔌 Infrastructure Subsystems Telemetry</h4>
            <p><strong>Database Engine:</strong> <span class="ws-badge ws-badge-brand">{health['database_status']}</span> ({health['database_connections']} Pool Connections Active)</p>
            <p><strong>Cache Subsystem:</strong> {health['cache_status']}</p>
            <p><strong>Background Queue:</strong> {health['queue_status']} ({health['active_background_jobs']} Active Jobs)</p>
        </div>
        """,
        unsafe_allow_html=True
    )
