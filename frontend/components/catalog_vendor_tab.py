"""
WatchSphere AI v3.0 - Vendor Management Catalog Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.vendor_service import VendorService
from backend.services.catalog_export_service import CatalogExportService
from backend.services.audit_log_service import AuditLogService
from frontend.components.cards import render_metric_card


def render_vendor_management_tab() -> None:
    """
    Renders clean Vendor Management workspace with Registration Form, Search/Filter, Data Table, and Audit Logs.
    """
    db = SessionLocal()
    try:
        vendor_service = VendorService(db)
        vendors = vendor_service.get_all()

        df_v = pd.DataFrame([
            {"company_name": v.company_name, "owner_name": v.owner_name, "email": v.email, "phone": v.phone, "gst_number": v.gst_number, "city": v.city, "state": v.state, "status": v.status}
            for v in vendors
        ]) if vendors else pd.DataFrame()

        st.markdown("### 🏬 Enterprise Vendor Management")

        # 1. Summary Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Total Vendors", f"{len(vendors)}", "Registered Suppliers", "Catalog")
        with c2:
            render_metric_card("Active Vendors", f"{len([v for v in vendors if v.status == 'Active'])}", "Active Status", "Active")
        with c3:
            render_metric_card("Top Supplier", "Acme Watch Co.", "Primary Vendor", "VIP")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Controls & Form
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])
        with ctrl_col1:
            search_query = st.text_input("🔍 Search Vendors...", key="vendor_search_input", placeholder="Company, Owner, Email, GST...")
        with ctrl_col2:
            show_register = st.button("➕ Register Vendor", type="primary", key="btn_open_reg_vendor", use_container_width=True)
        with ctrl_col3:
            show_audit = st.button("📜 Audit Log", key="btn_vendor_audit_log", use_container_width=True)

        if show_register or st.session_state.get("reg_vendor_open", False):
            st.session_state.reg_vendor_open = True
            with st.expander("📝 Register New Vendor Account", expanded=True):
                with st.form("form_register_vendor"):
                    f_col1, f_col2 = st.columns(2)
                    with f_col1:
                        v_comp = st.text_input("Company Name *", value="Apex Timepieces Ltd.")
                        v_owner = st.text_input("Owner Name *", value="Rahul Sharma")
                        v_email = st.text_input("Email Address *", value="contact@apextime.com")
                        v_phone = st.text_input("Phone Number *", value="+91 9876543210")
                        v_gst = st.text_input("GST Number *", value="27AAACA123411Z5")
                    with f_col2:
                        v_addr = st.text_input("Address", value="102 Corporate Park")
                        v_city = st.text_input("City *", value="Mumbai")
                        v_state = st.text_input("State *", value="Maharashtra")
                        v_country = st.text_input("Country *", value="India")
                        v_status = st.selectbox("Initial Status", options=["Active", "Suspended"])

                    submit_reg = st.form_submit_button("Submit Vendor Registration", type="primary")
                    if submit_reg:
                        v_dict = {"company_name": v_comp, "owner_name": v_owner, "email": v_email, "phone": v_phone, "gst_number": v_gst, "address": v_addr, "city": v_city, "state": v_state, "country": v_country, "status": v_status}
                        ok, msg, _ = vendor_service.create(v_dict)
                        if ok:
                            st.success(msg)
                            st.session_state.reg_vendor_open = False
                            st.rerun()
                        else:
                            st.error(msg)

        # Audit Log Dialog Modal
        if show_audit or st.session_state.get("vendor_audit_open", False):
            st.session_state.vendor_audit_open = True
            with st.expander("📜 Vendor Management Audit Trail", expanded=True):
                audit_service = AuditLogService(db)
                logs = audit_service.get_logs_for_entity("Vendor")
                if logs:
                    st.dataframe(pd.DataFrame([{"ID": l.id[:8], "Action": l.action, "Admin": l.admin_email, "Timestamp": l.created_at} for l in logs]), use_container_width=True)
                else:
                    st.info("No audit logs recorded for Vendor entity.")
                if st.button("Close Audit Log"):
                    st.session_state.vendor_audit_open = False
                    st.rerun()

        # 3. Data Table & Export
        st.markdown("### 📋 Registered Vendor Accounts Directory")
        if not df_v.empty:
            st.dataframe(df_v, use_container_width=True)
            csv_data = CatalogExportService.export_to_csv(df_v.to_dict(orient="records"))
            st.download_button("📥 Download Vendors CSV", data=csv_data, file_name="vendors_catalog_export.csv", mime="text/csv")

    finally:
        db.close()
