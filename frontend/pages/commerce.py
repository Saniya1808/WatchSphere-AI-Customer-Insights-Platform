"""
WatchSphere AI v3.0 - Enterprise Commerce BI Analytics Studio
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.utils.session import SessionManager
from frontend.components.footer import render_footer
from frontend.components.power_bi_filter_panel import render_power_bi_filter_panel
from frontend.components.commerce_customer_tab import render_customer_management_tab
from frontend.components.commerce_order_tab import render_order_management_tab
from frontend.components.commerce_inventory_tab import render_inventory_management_tab
from frontend.components.commerce_payment_tab import render_payment_management_tab
from frontend.components.commerce_review_tab import render_review_management_tab
from frontend.components.commerce_wishlist_tab import render_wishlist_management_tab
from frontend.components.commerce_analytics_tab import render_commerce_analytics_tab


def render_commerce_page() -> None:
    """
    Renders the upgraded Power BI Style Commerce Analytics Studio with 7 BI Workspaces:
    1. Customer BI Analytics Workspace
    2. Order BI Analytics Workspace
    3. Inventory BI Analytics Workspace
    4. Payment BI Analytics Workspace
    5. Review BI Analytics Workspace
    6. Wishlist BI Analytics Workspace
    7. Executive CEO Insights Workspace

    Enforces Role-Based Access Scoping for Admin vs Vendor users.
    """
    user_role = (SessionManager.get_user_role() or "").lower()

    st.markdown(
        f"""
        <div class="ws-breadcrumb">
            Home / <span>Commerce & Customer Intelligence</span>
        </div>
        <div style="margin-bottom: 16px;">
            <h1 style="font-family: var(--font-heading); font-size: 2.2rem; margin: 0; color: var(--text-main);">
                Power BI Enterprise Commerce Intelligence Studio
            </h1>
            <p style="color: var(--accent-indigo); font-size: 1rem; font-weight: 600; margin: 4px 0 0 0;">
                Tableau & Power BI Style Multidimensional Analytics Suite
                <span class="ws-badge ws-badge-brand" style="margin-left: 10px;">{user_role.upper()} PORTAL</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Power BI Slicer & Dynamic Filter Panel
    filter_state = render_power_bi_filter_panel()

    if user_role == "admin":
        tab_titles = [
            "👥 1. Customer BI Workspace",
            "📦 2. Order BI Workspace",
            "🏬 3. Inventory BI Workspace",
            "💳 4. Payment BI Workspace",
            "⭐ 5. Review BI Workspace",
            "💖 6. Wishlist BI Workspace",
            "👔 7. Executive CEO Insights"
        ]
    else:  # Vendor Role Scoped View
        tab_titles = [
            "📦 1. Vendor Orders BI",
            "🏬 2. Vendor Stock BI",
            "⭐ 3. Vendor Reviews BI",
            "👔 4. Vendor Sales BI"
        ]

    tabs = st.tabs(tab_titles)

    if user_role == "admin":
        with tabs[0]:
            render_customer_management_tab()
        with tabs[1]:
            render_order_management_tab()
        with tabs[2]:
            render_inventory_management_tab()
        with tabs[3]:
            render_payment_management_tab()
        with tabs[4]:
            render_review_management_tab()
        with tabs[5]:
            render_wishlist_management_tab()
        with tabs[6]:
            render_commerce_analytics_tab()
    else:
        with tabs[0]:
            render_order_management_tab()
        with tabs[1]:
            render_inventory_management_tab()
        with tabs[2]:
            render_review_management_tab()
        with tabs[3]:
            render_commerce_analytics_tab()

    render_footer()
