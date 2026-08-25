"""
WatchSphere AI v3.0 - AI Model Center & Lifecycle Management Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.ai_service import AIService


def render_ai_model_center_tab() -> None:
    """
    Renders AI Model Center tab with model registry table, retraining controls, and version history.
    """
    db = SessionLocal()
    try:
        ai_service = AIService(db)
        models = ai_service.get_registered_models()

        st.markdown("### ⚙️ Enterprise AI Model Registry & Lifecycle Management")

        if models:
            df_models = pd.DataFrame(models)
            st.dataframe(df_models, use_container_width=True)

            # Controls: Retrain
            st.markdown("#### ⚡ Retrain & Redeploy Model Pipeline")
            r_col1, r_col2 = st.columns([3, 1])
            with r_col1:
                sel_m_name = st.selectbox("Select Target Model for Retraining", options=[m["name"] for m in models], key="ai_model_retrain_select")
            with r_col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Retrain Model Now", type="primary", key="btn_exec_retrain_model"):
                    ok, msg = ai_service.retrain_model(sel_m_name)
                    st.success(msg)
                    st.rerun()

    finally:
        db.close()
