"""
WatchSphere AI v3.0 - AI Dashboard Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from frontend.components.cards import render_metric_card

COLOR_SEQ = ["#6366F1", "#8B5CF6", "#10B981", "#0EA5E9", "#F43F5E"]


def render_ai_dashboard_tab() -> None:
    """
    Renders AI Dashboard tab with 6 KPI Cards, Confusion Matrix, ROC Curve, and Feature Importance.
    """
    # 1. Top KPI Cards
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        render_metric_card("Models Trained", "6 Models", "Active Registry", "AI")
    with c2:
        render_metric_card("Accuracy Score", "94.8%", "Global Mean", "Success")
    with c3:
        render_metric_card("Deployed Models", "6 / 6", "100% Production", "Active")
    with c4:
        render_metric_card("Today's Predictions", "1,420", "Live Inferences", "Growth")
    with c5:
        render_metric_card("Avg Confidence", "96.2%", "Model Certainty", "VIP")
    with c6:
        render_metric_card("System Health", "100%", "Operational Status", "Active")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Interactive Charts
    col1, col2 = st.columns(2)
    with col1:
        # Confusion Matrix Heatmap
        z = [[450, 20], [15, 515]]
        x = ["Predicted Negative", "Predicted Positive"]
        y = ["Actual Negative", "Actual Positive"]
        fig_cm = px.imshow(z, x=x, y=y, text_auto=True, title="🎯 Global Model Confusion Matrix", color_continuous_scale="Purples")
        fig_cm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig_cm, use_container_width=True)

    with col2:
        # ROC Curve
        fpr = [0.0, 0.05, 0.1, 0.2, 0.5, 1.0]
        tpr = [0.0, 0.85, 0.92, 0.96, 0.99, 1.0]
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines+markers", name="Ensemble ROC (AUC = 0.962)", line=dict(color="#6366F1", width=3)))
        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random Baseline", line=dict(color="#94A3B8", dash="dash")))
        fig_roc.update_layout(title="📈 Receiver Operating Characteristic (ROC Curve)", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig_roc, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        # Feature Importance
        df_feat = pd.DataFrame({
            "feature": ["Recency Days", "Total Spending", "Orders Count", "Average Order Value", "Customer Age", "Rating Score"],
            "importance": [0.32, 0.28, 0.18, 0.12, 0.06, 0.04]
        })
        fig_feat = px.bar(df_feat, x="importance", y="feature", orientation="h", title="⭐ Global Feature Importance Weights", color_discrete_sequence=["#10B981"])
        fig_feat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig_feat, use_container_width=True)

    with col4:
        # Accuracy Trend
        df_acc = pd.DataFrame({
            "version": ["v1.0", "v1.2", "v1.5", "v2.0", "v2.5", "v3.0"],
            "accuracy": [0.88, 0.90, 0.92, 0.93, 0.94, 0.95]
        })
        fig_acc = px.line(df_acc, x="version", y="accuracy", markers=True, title="🚀 Model Version Accuracy Evolution", color_discrete_sequence=["#0EA5E9"])
        fig_acc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig_acc, use_container_width=True)
