"""
WatchSphere AI v3.0 - Customer Churn Prediction AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.customer_service import CustomerService
from ml.churn_prediction import ChurnPredictionEngine

COLOR_SEQ = ["#F43F5E", "#F59E0B", "#10B981"]


def render_ai_churn_tab() -> None:
    """
    Renders Churn Prediction tab with churn probabilities and retention action suggestions.
    """
    db = SessionLocal()
    try:
        cust_service = CustomerService(db)
        customers = cust_service.get_all()
        df_cust = pd.DataFrame([{"full_name": c.full_name, "email": c.email, "orders_count": c.orders_count, "last_purchase_days": 25} for c in customers]) if customers else pd.DataFrame()

        df_churn = ChurnPredictionEngine.predict_churn(df_cust)

        st.markdown("### ⚠️ Customer Churn Risk & Retention Intelligence")

        # Distribution Chart
        if not df_churn.empty:
            df_counts = df_churn["Risk Level"].value_counts().reset_index(name="count")
            fig = px.pie(df_counts, names="Risk Level", values="count", title="🎯 Churn Risk Level Distribution", color_discrete_sequence=COLOR_SEQ, hole=0.4)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 📋 Churn Risk Prediction Directory")
        st.dataframe(df_churn, use_container_width=True)

    finally:
        db.close()
