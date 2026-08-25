"""
WatchSphere AI v3.0 - Sales Forecasting AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from ml.sales_forecasting import SalesForecastingEngine
from backend.services.catalog_export_service import CatalogExportService
from frontend.components.cards import render_metric_card


def render_ai_sales_forecast_tab() -> None:
    """
    Renders Sales Forecasting tab with 7, 30, 90, 365 Days revenue prediction line and confidence bounds.
    """
    col_h, col_empty = st.columns([2, 2])
    with col_h:
        days_ahead = st.selectbox("Select Forecast Horizon", options=[7, 30, 90, 365], index=1, key="sales_forecast_days")

    res = SalesForecastingEngine.forecast_sales(days_ahead=days_ahead)
    df_fc = res["forecast_df"]
    metrics = res["model_metrics"]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Forecast", f"${res['total_forecasted_revenue']:,.2f}", f"Next {days_ahead} Days", "Revenue")
    with c2:
        render_metric_card("Avg Daily Revenue", f"${res['avg_daily_revenue']:,.2f}", "Predicted Mean", "Growth")
    with c3:
        render_metric_card("Model R² Score", f"{metrics['r2_score']}", "Fit Quality", "Active")
    with c4:
        render_metric_card("RMSE", f"${metrics['rmse']:.2f}", "Prediction Error", "Rating")

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Line Chart with Confidence Interval Band
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_fc["date"], y=df_fc["upper_confidence"], mode="lines", name="Upper Confidence (95%)", line=dict(width=0)))
    fig.add_trace(go.Scatter(x=df_fc["date"], y=df_fc["lower_confidence"], mode="lines", name="Lower Confidence (95%)", fill="tonexty", fillcolor="rgba(99, 102, 241, 0.15)", line=dict(width=0)))
    fig.add_trace(go.Scatter(x=df_fc["date"], y=df_fc["predicted_revenue"], mode="lines+markers", name="Predicted Daily Revenue", line=dict(color="#6366F1", width=3)))

    fig.update_layout(title=f"📈 Revenue Trajectory Forecast (Next {days_ahead} Days)", xaxis_title="Date", yaxis_title="Revenue ($)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
    st.plotly_chart(fig, use_container_width=True)

    # Data Table & Export
    st.markdown("### 📋 Daily Forecast Predictions Data Table")
    st.dataframe(df_fc, use_container_width=True)

    csv_fc = CatalogExportService.export_to_csv(df_fc.to_dict(orient="records"))
    st.download_button("📥 Download Revenue Predictions CSV", data=csv_fc, file_name=f"sales_forecast_{days_ahead}d.csv", mime="text/csv")
