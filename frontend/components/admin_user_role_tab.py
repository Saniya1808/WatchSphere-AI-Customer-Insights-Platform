"""
WatchSphere AI v3.0 - User & Role Management Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.user_service import UserService


def render_user_role_tab() -> None:
    """
    Renders User & Role Management tab with user directory, role assignment, and lock/unlock actions.
    """
    db = SessionLocal()
    try:
        user_service = UserService(db)
        users = user_service.get_all_users()

        st.markdown("### 👤 User Accounts & Role Governance")

        if users:
            u_rows = []
            for u in users:
                u_rows.append({
                    "ID": u.id[:8],
                    "Full Name": u.full_name,
                    "Email": u.email,
                    "Role": u.role,
                    "Vendor Company": u.vendor_company or "N/A",
                    "Status": "Active" if u.is_active else "Locked / Deactivated",
                    "Created Date": u.created_at
                })
            st.dataframe(pd.DataFrame(u_rows), use_container_width=True)

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                sel_u_email = st.selectbox("Target User", options=[u.email for u in users], key="user_adm_select")
            with col2:
                u_act = st.selectbox("Action", options=["Lock Account", "Unlock Account", "Reset Password", "Delete Account"], key="user_adm_action")
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Execute Action", type="primary", key="btn_exec_user_adm"):
                    target_u = next((u for u in users if u.email == sel_u_email), None)
                    if target_u:
                        if u_act == "Lock Account":
                            ok, msg = user_service.lock_account(target_u.id)
                            st.toast(msg)
                            st.rerun()
                        elif u_act == "Unlock Account":
                            ok, msg = user_service.unlock_account(target_u.id)
                            st.toast(msg)
                            st.rerun()
                        elif u_act == "Reset Password":
                            ok, msg = user_service.reset_password(target_u.id)
                            st.toast(msg)
                            st.rerun()
                        elif u_act == "Delete Account":
                            ok, msg = user_service.delete_user(target_u.id)
                            st.toast(msg)
                            st.rerun()

    finally:
        db.close()
