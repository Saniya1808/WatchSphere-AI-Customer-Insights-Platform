"""
WatchSphere AI v3.0 - API Management Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.api_management_service import APIManagementService


def render_api_management_tab() -> None:
    """
    Renders API Management tab connected to APIManagementService.
    """
    db = SessionLocal()
    try:
        api_service = APIManagementService(db)
        keys = api_service.get_keys()

        st.markdown("### 🔑 REST API Key Governance & Token Management")

        col1, col2 = st.columns([3, 1])
        with col1:
            key_name = st.text_input("New API Key Description", value="Partner Vendor API Key", key="api_key_name_input")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Generate API Key", type="primary", key="btn_exec_gen_api_key"):
                ok, msg, created_k = api_service.generate_api_key(key_name)
                st.success(msg)
                st.code(f"API_KEY: {created_k.api_key_hash}")
                st.rerun()

        st.markdown("#### 📋 Registered API Tokens Directory")
        if keys:
            k_rows = [{"ID": k.id[:8], "Description": k.key_name, "API Key": f"{k.api_key_hash[:12]}...", "Rate Limit": f"{k.rate_limit_per_min} req/min", "Status": k.status, "Created Date": k.created_at} for k in keys]
            st.dataframe(pd.DataFrame(k_rows), use_container_width=True)

            # Revoke API Key Action
            col_sel, col_act = st.columns([3, 1])
            with col_sel:
                sel_k_id = st.selectbox("Select Key to Revoke", options=[k.id for k in keys if k.status == "Active"], key="api_revoke_select")
            with col_act:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Revoke Key", key="btn_exec_revoke_api_key"):
                    if sel_k_id:
                        ok, msg = api_service.revoke_key(sel_k_id)
                        st.toast(msg)
                        st.rerun()

    finally:
        db.close()
