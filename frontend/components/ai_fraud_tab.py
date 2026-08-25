"""
WatchSphere AI v3.0 - Fraud Detection AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.order_service import OrderService
from ml.fraud_detection import FraudDetectionEngine


def render_ai_fraud_tab() -> None:
    """
    Renders Fraud Detection tab with Isolation Forest anomaly scores and suspicious order alerts.
    """
    db = SessionLocal()
    try:
        order_service = OrderService(db)
        orders = order_service.get_all()
        df_orders = pd.DataFrame([{"order_number": o.order_number, "customer_name": o.customer_name, "total_amount": o.total_amount, "items_count": o.items_count, "payment_method": o.payment_method} for o in orders]) if orders else pd.DataFrame()

        df_fraud = FraudDetectionEngine.detect_fraud(df_orders)

        st.markdown("### 🚨 Isolation Forest Transaction Anomaly & Fraud Scoring")

        if not df_fraud.empty:
            susp_count = len(df_fraud[df_fraud["is_suspicious"] == "High Risk Anomaly"])
            st.error(f"⚠️ **{susp_count} Anomaly Transactions Flagged** as High Risk Suspicious Orders!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_fraud, use_container_width=True)

    finally:
        db.close()
