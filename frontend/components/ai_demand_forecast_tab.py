"""
WatchSphere AI v3.0 - Demand Forecasting AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.product_service import ProductService
from ml.demand_forecasting import DemandForecastingEngine


def render_ai_demand_forecast_tab() -> None:
    """
    Renders Demand Forecasting tab with stockout date predictions and recommended reorder quantities.
    """
    db = SessionLocal()
    try:
        prd_service = ProductService(db)
        products = prd_service.get_all()
        df_prd = pd.DataFrame([{"sku": p.sku, "name": p.name, "current_stock": p.current_stock, "minimum_stock": p.minimum_stock} for p in products]) if products else pd.DataFrame()

        df_demand = DemandForecastingEngine.forecast_product_demand(df_prd)

        st.markdown("### 📦 Predictive Inventory Demand & Stockout Schedule")
        
        crit_count = len(df_demand[df_demand["Risk Status"] == "CRITICAL"]) if "Risk Status" in df_demand.columns else 0
        warn_count = len(df_demand[df_demand["Risk Status"] == "WARNING"]) if "Risk Status" in df_demand.columns else 0

        col1, col2 = st.columns(2)
        with col1:
            st.warning(f"⚠️ **{crit_count} Products** predicted to reach stockout within 2 days.")
        with col2:
            st.info(f"💡 **{warn_count} Products** reaching stockout within 7 days.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_demand, use_container_width=True)

    finally:
        db.close()
