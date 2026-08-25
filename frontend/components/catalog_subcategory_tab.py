"""
WatchSphere AI v3.0 - Subcategory Management Catalog Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.category_service import CategoryService
from backend.services.catalog_export_service import CatalogExportService


def render_subcategory_management_tab() -> None:
    """
    Renders clean Subcategory Management workspace with Creation Form, Filter, and Data Table.
    """
    db = SessionLocal()
    try:
        cat_service = CategoryService(db)
        subcategories = cat_service.get_all_subcategories()
        categories = cat_service.get_all_categories()

        df_sub = pd.DataFrame([
            {"name": s.name, "parent_category_name": s.parent_category_name, "description": s.description, "products_count": s.products_count, "status": s.status}
            for s in subcategories
        ]) if subcategories else pd.DataFrame()

        st.markdown("### 📂 Product Sub Category Management")

        # Search & Form Controls
        col_search, col_btn = st.columns([3, 1])
        with col_search:
            parent_filter = st.selectbox("Filter by Parent Category", options=["All Categories"] + [c.name for c in categories], key="subcat_parent_filter")
        with col_btn:
            show_create_sub = st.button("➕ Create Subcategory", type="primary", key="btn_open_create_subcat", use_container_width=True)

        if show_create_sub or st.session_state.get("create_subcat_open", False):
            st.session_state.create_subcat_open = True
            with st.expander("📂 Create New Subcategory", expanded=True):
                with st.form("form_create_subcategory"):
                    s_name = st.text_input("Subcategory Name *", value="Solar Powered Digital")
                    s_parent_name = st.selectbox("Parent Category *", options=[c.name for c in categories])
                    s_desc = st.text_area("Description", value="Eco-friendly solar powered timepieces.")
                    s_status = st.selectbox("Status", options=["Active", "Hidden"])

                    submit_sub = st.form_submit_button("Create Subcategory", type="primary")
                    if submit_sub:
                        parent_obj = next((c for c in categories if c.name == s_parent_name), None)
                        if parent_obj:
                            s_dict = {"name": s_name, "parent_category_id": parent_obj.id, "description": s_desc, "status": s_status}
                            ok, msg, _ = cat_service.create_subcategory(s_dict)
                            if ok:
                                st.success(msg)
                                st.session_state.create_subcat_open = False
                                st.rerun()
                            else:
                                st.error(msg)

        # Data Table
        st.markdown("### 📂 Catalog Subcategories Directory")
        if not df_sub.empty:
            st.dataframe(df_sub, use_container_width=True)
            csv_data = CatalogExportService.export_to_csv(df_sub.to_dict(orient="records"))
            st.download_button("📥 Download Subcategories CSV", data=csv_data, file_name="subcategories_catalog_export.csv", mime="text/csv")

    finally:
        db.close()
