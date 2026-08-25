"""
WatchSphere AI v3.0 - Enterprise Catalog Management Studio
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.utils.session import SessionManager
from frontend.components.footer import render_footer
from frontend.components.catalog_vendor_tab import render_vendor_management_tab
from frontend.components.catalog_category_tab import render_category_management_tab
from frontend.components.catalog_subcategory_tab import render_subcategory_management_tab
from frontend.components.catalog_product_tab import render_product_management_tab


def render_catalog_page() -> None:
    """
    Renders the complete Enterprise Catalog Management Studio with 4 Enterprise Modules:
    1. Vendor Management
    2. Category Management
    3. Sub Category Management
    4. Product Management

    Protected by RBAC Access Guard (Admin only).
    """
    user_role = (SessionManager.get_user_role() or "").lower()

    if user_role != "admin":
        st.markdown(
            """
            <div class="ws-glass-card" style="border-left: 5px solid #F43F5E; padding: 40px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 12px;">🚫</div>
                <h2 style="font-family: var(--font-heading); color: #F43F5E; margin: 0 0 10px 0;">
                    Access Restricted — Admin Only
                </h2>
                <p style="color: var(--text-sub); max-width: 500px; margin: 0 auto 16px auto; font-size: 1rem;">
                    The Enterprise Catalog Management Studio is restricted exclusively to Administrator accounts.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        render_footer()
        return

    st.markdown(
        """
        <div class="ws-breadcrumb">
            Home / <span>Catalog Management</span>
        </div>
        <div style="margin-bottom: 16px;">
            <h1 style="font-family: var(--font-heading); font-size: 2.2rem; margin: 0; color: var(--text-main);">
                Enterprise Catalog Management Studio
            </h1>
            <p style="color: var(--accent-indigo); font-size: 1rem; font-weight: 600; margin: 4px 0 0 0;">
                Vendor Directory, Category Hierarchy & Product Registration Suite
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_vendor, tab_category, tab_subcategory, tab_product = st.tabs([
        "🏬 1. Vendor Management",
        "📁 2. Category Management",
        "📂 3. Sub Category Management",
        "⌚ 4. Product Management"
    ])

    with tab_vendor:
        render_vendor_management_tab()

    with tab_category:
        render_category_management_tab()

    with tab_subcategory:
        render_subcategory_management_tab()

    with tab_product:
        render_product_management_tab()

    render_footer()
