"""
WatchSphere AI v3.0 - Category Management Catalog Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.category_service import CategoryService
from backend.services.catalog_export_service import CatalogExportService
from frontend.components.cards import render_metric_card


def render_category_management_tab() -> None:
    """
    Renders clean Category Management workspace with Creation Form, Search Bar, and Data Table.
    """
    db = SessionLocal()
    try:
        cat_service = CategoryService(db)
        categories = cat_service.get_all_categories()

        df_cat = pd.DataFrame([
            {"name": c.name, "description": c.description, "display_order": c.display_order, "status": c.status, "products_count": c.products_count}
            for c in categories
        ]) if categories else pd.DataFrame()

        st.markdown("### 📁 Product Category Management")

        # 1. Summary Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Total Categories", f"{len(categories)}", "Main Divisions", "Catalog")
        with c2:
            render_metric_card("Active Categories", f"{len([c for c in categories if c.status == 'Active'])}", "Visible in Portal", "Active")
        with c3:
            render_metric_card("Top Category", "Smartwatches", "Most SKUs", "VIP")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Search & Form Controls
        col_search, col_btn = st.columns([3, 1])
        with col_search:
            cat_search = st.text_input("🔍 Search Categories...", key="cat_search_input")
        with col_btn:
            show_create = st.button("➕ Create Category", type="primary", key="btn_open_create_cat", use_container_width=True)

        if show_create or st.session_state.get("create_cat_open", False):
            st.session_state.create_cat_open = True
            with st.expander("📁 Create New Product Category", expanded=True):
                with st.form("form_create_category"):
                    c_name = st.text_input("Category Name *", value="Luxury Hybrid Watches")
                    c_desc = st.text_area("Description", value="Premium hybrid mechanical smartwatches.")
                    c_order = st.number_input("Display Order", min_value=1, value=1)
                    c_status = st.selectbox("Status", options=["Active", "Hidden"])

                    submit_cat = st.form_submit_button("Create Category", type="primary")
                    if submit_cat:
                        c_dict = {"name": c_name, "description": c_desc, "display_order": c_order, "status": c_status}
                        ok, msg, _ = cat_service.create_category(c_dict)
                        if ok:
                            st.success(msg)
                            st.session_state.create_cat_open = False
                            st.rerun()
                        else:
                            st.error(msg)

        # 3. Data Table
        st.markdown("### 📁 Product Categories Directory")
        if not df_cat.empty:
            st.dataframe(df_cat, use_container_width=True)
            csv_data = CatalogExportService.export_to_csv(df_cat.to_dict(orient="records"))
            st.download_button("📥 Download Categories CSV", data=csv_data, file_name="categories_catalog_export.csv", mime="text/csv")

    finally:
        db.close()
