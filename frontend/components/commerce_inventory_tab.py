"""
WatchSphere AI v3.0 - Inventory BI Analytics Workspace Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.product_service import ProductService
from backend.services.inventory_service import InventoryService
from backend.services.commerce_bi_analytics_service import CommerceBIAnalyticsService
from frontend.components.cards import render_metric_card


def render_inventory_management_tab() -> None:
    """
    Renders Inventory BI Analytics Workspace with ABC/XYZ Matrix, Stock Turnover, and Warehouse Distribution.
    Calculates stock levels dynamically from real database product records.
    """
    db = SessionLocal()
    try:
        product_service = ProductService(db)
        inventory_service = InventoryService(db)

        products = product_service.get_all()
        df_prd = pd.DataFrame([
            {"sku": p.sku, "name": p.name, "brand": p.brand, "warehouse": p.warehouse, "selling_price": p.selling_price, "current_stock": p.current_stock, "minimum_stock": p.minimum_stock}
            for p in products
        ]) if products else pd.DataFrame()

        tot_prods = len(products)
        tot_stock = df_prd['current_stock'].sum() if not df_prd.empty else 0
        low_stock = len([p for p in products if p.current_stock < p.minimum_stock])
        out_of_stock = len([p for p in products if p.current_stock == 0])
        warehouses_cnt = len(set(p.warehouse for p in products if p.warehouse))

        # 1. 5 Executive KPIs
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Total Products", f"{tot_prods:,}", "Catalog SKUs", "Inventory")
        with c2:
            render_metric_card("Available Stock", f"{tot_stock:,}", "Units On Hand", "Units")
        with c3:
            render_metric_card("Low Stock Alert", f"{low_stock:,}", "Below Min Level", "Warning")
        with c4:
            render_metric_card("Out of Stock", f"{out_of_stock:,}", "Zero Stock Items", "Danger")
        with c5:
            render_metric_card("Warehouses", f"{warehouses_cnt} Hubs", "Regional Centers", "Warehouse")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. ABC / XYZ Analysis & Warehouse Distribution
        col1, col2 = st.columns(2)
        with col1:
            if not df_prd.empty:
                df_abc = CommerceBIAnalyticsService.get_abc_xyz_analysis(df_prd)
                fig_abc = px.pie(df_abc, names="abc_category", title="📦 ABC Inventory Revenue Matrix", color_discrete_sequence=px.colors.qualitative.Prism, hole=0.4)
                fig_abc.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_abc, use_container_width=True)

        with col2:
            if not df_prd.empty and "warehouse" in df_prd.columns:
                df_wh = df_prd.groupby("warehouse")["current_stock"].sum().reset_index()
                df_wh.columns = ["Warehouse Hub", "Total Stock Units"]
                fig_wh = px.bar(df_wh, x="Warehouse Hub", y="Total Stock Units", title="🏬 Stock Distribution across Regional Warehouses", color_discrete_sequence=["#F59E0B"])
                fig_wh.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_wh, use_container_width=True)

        # 3. Inventory Table
        st.markdown("### 🏬 Regional Warehouse Stock Directory")
        if not df_prd.empty:
            st.dataframe(df_prd, use_container_width=True)

    finally:
        db.close()
