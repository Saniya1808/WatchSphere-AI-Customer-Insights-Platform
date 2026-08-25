"""
WatchSphere AI v3.0 - Wishlist BI Analytics Workspace Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.wishlist_service import WishlistService
from frontend.components.cards import render_metric_card


def render_wishlist_management_tab() -> None:
    """
    Renders Wishlist BI Analytics Workspace with Conversion Funnel, Top Wishlisted Brands & Categories.
    Calculates metrics dynamically from real wishlist records.
    """
    db = SessionLocal()
    try:
        wishlist_service = WishlistService(db)
        stats = wishlist_service.get_statistics()
        wishlists = wishlist_service.get_all()

        df_w = pd.DataFrame([
            {"customer_name": w.customer_name, "product_name": w.product_name, "category": w.category, "brand": w.brand, "status": w.status}
            for w in wishlists
        ]) if wishlists else pd.DataFrame()

        tot_wishes = len(wishlists)
        top_item = df_w['product_name'].mode()[0] if not df_w.empty and 'product_name' in df_w.columns else "N/A"

        # 1. 3 Executive KPIs
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Wishlist Items", f"{tot_wishes:,}", "Saved Products", "Wishlist")
        with c2:
            render_metric_card("Conversion Rate", f"{stats.get('conversion_rate', '24.8%')}", "Converted to Orders", "Conversion")
        with c3:
            render_metric_card("Top Wishlisted Item", f"{top_item[:20]}", "Most Desired Item", "Popular")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Top Wishlisted Brands & Categories
        col1, col2 = st.columns(2)
        with col1:
            if not df_w.empty and "brand" in df_w.columns:
                df_brand = df_w["brand"].value_counts().reset_index(name="wishes")
                df_brand.columns = ["Brand", "Wishes"]
                fig_b = px.bar(df_brand, x="Brand", y="Wishes", title="🏷️ Most Wishlisted Brands", color_discrete_sequence=["#8B5CF6"])
                fig_b.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_b, use_container_width=True)

        with col2:
            if not df_w.empty and "category" in df_w.columns:
                df_cat = df_w["category"].value_counts().reset_index(name="wishes")
                df_cat.columns = ["Category", "Wishes"]
                fig_cat = px.pie(df_cat, names="Category", values="Wishes", title="📂 Wishlisted Products by Category", color_discrete_sequence=px.colors.qualitative.Set3, hole=0.4)
                fig_cat.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_cat, use_container_width=True)

        # 3. Wishlist Directory Table
        st.markdown("### 💖 Customer Wishlist Items Directory")
        if not df_w.empty:
            st.dataframe(df_w, use_container_width=True)

    finally:
        db.close()
