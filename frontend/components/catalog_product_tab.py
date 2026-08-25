"""
WatchSphere AI v3.0 - Product Management Catalog Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import uuid
import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.product_service import ProductService
from backend.services.vendor_service import VendorService
from backend.services.category_service import CategoryService
from backend.services.catalog_export_service import CatalogExportService
from backend.services.audit_log_service import AuditLogService
from frontend.components.cards import render_metric_card


def render_product_management_tab() -> None:
    """
    Renders clean Product Management workspace with Registration Form, Image Upload, SKU Search, Data Table, and Audit Logs.
    """
    db = SessionLocal()
    try:
        product_service = ProductService(db)
        vendor_service = VendorService(db)
        cat_service = CategoryService(db)

        products = product_service.get_all()
        vendors = vendor_service.get_all()
        categories = cat_service.get_all_categories()

        df_prd = pd.DataFrame([
            {
                "sku": p.sku, "name": p.name, "brand": p.brand, "vendor_name": p.vendor_name,
                "category_name": p.category_name, "cost_price": p.cost_price, "selling_price": p.selling_price,
                "profit_margin": p.profit_margin, "current_stock": p.current_stock, "status": p.status
            }
            for p in products
        ]) if products else pd.DataFrame()

        st.markdown("### ⌚ Enterprise Product Catalog Management")

        # 1. Summary Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Total Products", f"{len(df_prd)}", "Catalog SKUs", "Catalog")
        with c2:
            render_metric_card("Available Stock", f"{df_prd['current_stock'].sum() if not df_prd.empty else 0:,}", "Units On Hand", "Units")
        with c3:
            render_metric_card("Average Margin", f"{df_prd['profit_margin'].mean() if not df_prd.empty else 58.4:.1f}%", "Profit Margin", "Success")
        with c4:
            render_metric_card("Active Status", f"{len([p for p in products if p.status == 'Active'])}", "Live Items", "Active")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Controls & Form
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])
        with ctrl_col1:
            search_query = st.text_input("🔍 Search Catalog Products...", key="product_search_input", placeholder="Name, SKU, Brand, Vendor...")
        with ctrl_col2:
            show_register = st.button("➕ Register Product", type="primary", key="btn_open_reg_product", use_container_width=True)
        with ctrl_col3:
            show_audit = st.button("📜 Product Audit", key="btn_product_audit_log", use_container_width=True)

        if show_register or st.session_state.get("reg_product_open", False):
            st.session_state.reg_product_open = True
            with st.expander("⌚ Register New Product SKU", expanded=True):
                with st.form("form_register_product"):
                    f_col1, f_col2 = st.columns(2)
                    with f_col1:
                        p_sku = st.text_input("SKU Number *", value=f"SKU-{uuid.uuid4().hex[:6].upper()}")
                        p_name = st.text_input("Product Name *", value="WatchSphere Pro Ultra 3")
                        p_brand = st.text_input("Brand *", value="WatchSphere")
                        p_vendor = st.selectbox("Vendor *", options=[v.company_name for v in vendors])
                        p_cat = st.selectbox("Category *", options=[c.name for c in categories])
                    with f_col2:
                        p_cost = st.number_input("Cost Price ($)", min_value=1.0, value=250.0)
                        p_sell = st.number_input("Selling Price ($)", min_value=1.0, value=599.0)
                        p_stock = st.number_input("Current Stock Units", min_value=0, value=50)
                        p_min_stock = st.number_input("Minimum Stock Alert Level", min_value=1, value=5)
                        p_status = st.selectbox("Status", options=["Active", "Draft", "Archived"])

                    submit_reg = st.form_submit_button("Register Product SKU", type="primary")
                    if submit_reg:
                        vendor_obj = next((v for v in vendors if v.company_name == p_vendor), None)
                        cat_obj = next((c for c in categories if c.name == p_cat), None)
                        if vendor_obj and cat_obj:
                            margin_val = round(((p_sell - p_cost) / p_sell) * 100, 2)
                            p_dict = {
                                "sku": p_sku, "name": p_name, "brand": p_brand, "vendor_id": vendor_obj.id,
                                "category_id": cat_obj.id, "cost_price": p_cost, "selling_price": p_sell,
                                "profit_margin": margin_val, "current_stock": p_stock, "minimum_stock": p_min_stock,
                                "status": p_status
                            }
                            ok, msg, _ = product_service.create(p_dict)
                            if ok:
                                st.success(msg)
                                st.session_state.reg_product_open = False
                                st.rerun()
                            else:
                                st.error(msg)

        # Audit Log Dialog Modal
        if show_audit or st.session_state.get("product_audit_open", False):
            st.session_state.product_audit_open = True
            with st.expander("📜 Product Management Audit Trail", expanded=True):
                audit_service = AuditLogService(db)
                logs = audit_service.get_logs_for_entity("Product")
                if logs:
                    st.dataframe(pd.DataFrame([{"ID": l.id[:8], "Action": l.action, "Admin": l.admin_email, "Timestamp": l.created_at} for l in logs]), use_container_width=True)
                else:
                    st.info("No audit logs recorded for Product entity.")
                if st.button("Close Audit Log"):
                    st.session_state.product_audit_open = False
                    st.rerun()

        # 3. Data Table & Export
        st.markdown("### ⌚ Catalog Products Directory")
        if not df_prd.empty:
            st.dataframe(df_prd, use_container_width=True)
            csv_data = CatalogExportService.export_to_csv(df_prd.to_dict(orient="records"))
            st.download_button("📥 Download Products CSV", data=csv_data, file_name="products_catalog_export.csv", mime="text/csv")

    finally:
        db.close()
