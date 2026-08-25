"""
WatchSphere AI v3.0 - Executive Sales Analytics Plotly Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from backend.services.analytics_service import AnalyticsService

# Glassmorphic Plotly Theme Colors
DARK_BG = "rgba(15, 23, 42, 0.0)"
TEXT_COLOR = "#F8FAFC"
COLOR_SEQUENCE = ["#6366F1", "#8B5CF6", "#10B981", "#0EA5E9", "#F43F5E", "#F59E0B"]


def update_chart_layout(fig, title: str):
    """Applies unified dark/light glassmorphism styling to Plotly figures."""
    fig.update_layout(
        title={"text": title, "font": {"size": 16, "color": TEXT_COLOR, "family": "Plus Jakarta Sans"}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_COLOR, "family": "Inter"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.2, "xanchor": "center", "x": 0.5}
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    return fig


def render_executive_analytics_suite(df_orders: pd.DataFrame, df_inventory: pd.DataFrame) -> None:
    """
    Renders 11 Plotly interactive analytics charts in responsive 2-column grid layout.
    """
    st.markdown("### 📊 Executive Sales Analytics")

    # 1 & 2: Revenue Trend & Order Volume
    col1, col2 = st.columns(2)
    with col1:
        df_monthly = AnalyticsService.get_monthly_revenue_trend(df_orders)
        if not df_monthly.empty:
            fig1 = px.area(
                df_monthly, x="Month", y="Revenue",
                color_discrete_sequence=["#6366F1"],
                labels={"Revenue": "Gross Revenue ($)"}
            )
            update_chart_layout(fig1, "📈 Monthly Revenue Trend (Area)")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No monthly revenue data available.")

    with col2:
        if not df_monthly.empty:
            fig2 = px.bar(
                df_monthly, x="Month", y="Orders",
                color_discrete_sequence=["#0EA5E9"],
                labels={"Orders": "Order Volume"}
            )
            update_chart_layout(fig2, "📊 Monthly Order Volume (Bar)")
            st.plotly_chart(fig2, use_container_width=True)

    # 3 & 4: Category & Vendor Revenue
    col3, col4 = st.columns(2)
    with col3:
        df_cat = AnalyticsService.get_revenue_by_category(df_orders)
        if not df_cat.empty:
            fig3 = px.pie(
                df_cat, names="category", values="total_revenue",
                hole=0.5, color_discrete_sequence=COLOR_SEQUENCE
            )
            update_chart_layout(fig3, "🍩 Revenue by Category (Donut)")
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        df_vend = AnalyticsService.get_revenue_by_vendor(df_orders)
        if not df_vend.empty:
            fig4 = px.bar(
                df_vend, x="total_revenue", y="vendor_name", orientation="h",
                color_discrete_sequence=["#8B5CF6"],
                labels={"total_revenue": "Revenue ($)", "vendor_name": "Vendor"}
            )
            update_chart_layout(fig4, "🏬 Revenue by Vendor (Horizontal Bar)")
            st.plotly_chart(fig4, use_container_width=True)

    # 5 & 6: City Revenue & Payment Method
    col5, col6 = st.columns(2)
    with col5:
        df_city = AnalyticsService.get_revenue_by_city(df_orders)
        if not df_city.empty:
            fig5 = px.bar(
                df_city, x="city", y="total_revenue",
                color_discrete_sequence=["#10B981"],
                labels={"total_revenue": "Revenue ($)", "city": "City"}
            )
            update_chart_layout(fig5, "🏙️ Revenue by City (Bar)")
            st.plotly_chart(fig5, use_container_width=True)

    with col6:
        df_pay = AnalyticsService.get_revenue_by_payment_method(df_orders)
        if not df_pay.empty:
            fig6 = px.pie(
                df_pay, names="payment_method", values="total_revenue",
                hole=0.4, color_discrete_sequence=COLOR_SEQUENCE
            )
            update_chart_layout(fig6, "💳 Revenue by Payment Method (Donut)")
            st.plotly_chart(fig6, use_container_width=True)

    # 7 & 8: Top 10 & Bottom 10 Products
    col7, col8 = st.columns(2)
    with col7:
        df_top = AnalyticsService.get_top_products(df_orders, top_n=10)
        if not df_top.empty:
            fig7 = px.bar(
                df_top, x="total_revenue", y="product_name", orientation="h",
                color_discrete_sequence=["#6366F1"],
                labels={"total_revenue": "Revenue ($)", "product_name": "Product"}
            )
            update_chart_layout(fig7, "🔥 Top 10 Revenue Generating Products")
            st.plotly_chart(fig7, use_container_width=True)

    with col8:
        df_bot = AnalyticsService.get_bottom_products(df_orders, bottom_n=10)
        if not df_bot.empty:
            fig8 = px.bar(
                df_bot, x="total_revenue", y="product_name", orientation="h",
                color_discrete_sequence=["#F59E0B"],
                labels={"total_revenue": "Revenue ($)", "product_name": "Product"}
            )
            update_chart_layout(fig8, "⚠️ Bottom 10 Lowest Revenue Products")
            st.plotly_chart(fig8, use_container_width=True)

    # 9, 10 & 11: Distributions & Warehouse Treemap
    col9, col10 = st.columns(2)
    with col9:
        df_ord_status = AnalyticsService.get_order_status_distribution(df_orders)
        if not df_ord_status.empty:
            fig9 = px.pie(
                df_ord_status, names="order_status", values="count",
                hole=0.4, color_discrete_sequence=COLOR_SEQUENCE
            )
            update_chart_layout(fig9, "📦 Order Status Distribution (Donut)")
            st.plotly_chart(fig9, use_container_width=True)

    with col10:
        df_wh = AnalyticsService.get_inventory_by_warehouse(df_inventory)
        if not df_wh.empty:
            fig11 = px.treemap(
                df_wh, path=["warehouse"], values="inventory_value",
                color_discrete_sequence=COLOR_SEQUENCE
            )
            update_chart_layout(fig11, "🏭 Inventory Value by Warehouse (Treemap)")
            st.plotly_chart(fig11, use_container_width=True)
