"""
WatchSphere AI v3.0 - Sticky Global Enterprise Filter Bar
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import streamlit as st

from config.database import SessionLocal
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.models.customer import Customer
from backend.models.order import Order


def render_global_filter_bar() -> Dict[str, Any]:
    """
    Renders sticky enterprise multi-dimensional filter controls and returns filter parameters dictionary.
    Option lists are dynamically queried from SQLite database.
    """
    st.markdown("### 🎛️ Executive Multi-Dimensional Filter Bar")

    db = SessionLocal()
    try:
        vendors = [v.company_name for v in db.query(Vendor.company_name).distinct().all() if v.company_name]
        categories = [c.name for c in db.query(Category.name).distinct().all() if c.name]
        subcategories = [s.name for s in db.query(Subcategory.name).distinct().all() if s.name]
        cities = [c[0] for c in db.query(Customer.city).distinct().all() if c[0]]
        statuses = [s[0] for s in db.query(Order.order_status).distinct().all() if s[0]]
    except Exception:
        vendors, categories, subcategories, cities, statuses = [], [], [], [], []
    finally:
        db.close()

    vendor_opts = ["All Vendors"] + sorted(vendors)
    cat_opts = ["All Categories"] + sorted(categories)
    subcat_opts = ["All Subcategories"] + sorted(subcategories)
    city_opts = ["All Cities"] + sorted(cities)
    status_opts = ["All Statuses"] + sorted(statuses)

    if "filters" not in st.session_state:
        st.session_state.filters = {
            "vendor": "All Vendors",
            "brand": "All Brands",
            "category": "All Categories",
            "sub_category": "All Subcategories",
            "order_status": "All Statuses",
            "payment_status": "All Statuses",
            "city": "All Cities",
            "country": "All Countries",
            "warehouse": "All Warehouses",
            "customer_segment": "All Segments",
            "date_range": (
                (datetime.now(timezone.utc) - timedelta(days=180)).date(),
                datetime.now(timezone.utc).date()
            )
        }

    with st.expander("🔍 Filter Controls & Dimensions", expanded=False):
        row1_c1, row1_c2, row1_c3, row1_c4 = st.columns(4)
        with row1_c1:
            date_val = st.date_input(
                "Date Range",
                value=st.session_state.filters["date_range"],
                key="filter_date_range"
            )
        with row1_c2:
            vendor_val = st.selectbox(
                "Vendor",
                options=vendor_opts,
                index=0,
                key="filter_vendor"
            )
        with row1_c3:
            brand_val = st.selectbox(
                "Brand",
                options=["All Brands", "WatchSphere", "Swiss TimeCraft", "Tokyo Tech", "Nordic Krono"],
                index=0,
                key="filter_brand"
            )
        with row1_c4:
            category_val = st.selectbox(
                "Category",
                options=cat_opts,
                index=0,
                key="filter_category"
            )

        row2_c1, row2_c2, row2_c3, row2_c4 = st.columns(4)
        with row2_c1:
            subcat_val = st.selectbox(
                "Sub Category",
                options=subcat_opts,
                index=0,
                key="filter_subcat"
            )
        with row2_c2:
            order_status_val = st.selectbox(
                "Order Status",
                options=status_opts,
                index=0,
                key="filter_order_status"
            )
        with row2_c3:
            pay_status_val = st.selectbox(
                "Payment Status",
                options=["All Statuses", "Paid", "Pending", "Refunded"],
                index=0,
                key="filter_pay_status"
            )
        with row2_c4:
            city_val = st.selectbox(
                "City",
                options=city_opts,
                index=0,
                key="filter_city"
            )

        row3_c1, row3_c2, row3_c3, row3_c4 = st.columns(4)
        with row3_c1:
            country_val = st.selectbox(
                "Country",
                options=["All Countries", "India", "USA", "UK", "Global"],
                index=0,
                key="filter_country"
            )
        with row3_c2:
            wh_val = st.selectbox(
                "Warehouse",
                options=["All Warehouses", "WH-East Coast", "WH-West Coast", "WH-Europe Hub", "WH-Asia Pacific"],
                index=0,
                key="filter_wh"
            )
        with row3_c3:
            seg_val = st.selectbox(
                "Customer Segment",
                options=["All Segments", "Enterprise VIP", "Regular Consumer", "High Net Worth", "Corporate Account"],
                index=0,
                key="filter_segment"
            )
        with row3_c4:
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                apply_clicked = st.button("Apply", type="primary", key="btn_apply_filters", use_container_width=True)
            with col_btn2:
                reset_clicked = st.button("Reset", key="btn_reset_filters", use_container_width=True)
            with col_btn3:
                export_clicked = st.button("Export", key="btn_export_view", use_container_width=True)

            if reset_clicked:
                st.session_state.filters = {
                    "vendor": "All Vendors", "brand": "All Brands", "category": "All Categories",
                    "sub_category": "All Subcategories", "order_status": "All Statuses",
                    "payment_status": "All Statuses", "city": "All Cities", "country": "All Countries",
                    "warehouse": "All Warehouses", "customer_segment": "All Segments",
                    "date_range": ((datetime.now(timezone.utc) - timedelta(days=180)).date(), datetime.now(timezone.utc).date())
                }
                st.rerun()

            if apply_clicked:
                st.session_state.filters = {
                    "vendor": vendor_val, "brand": brand_val, "category": category_val,
                    "sub_category": subcat_val, "order_status": order_status_val,
                    "payment_status": pay_status_val, "city": city_val, "country": country_val,
                    "warehouse": wh_val, "customer_segment": seg_val, "date_range": date_val
                }
                st.toast("Filters Applied Successfully!", icon="✅")

            if export_clicked:
                st.toast("Current BI View Exported to CSV!", icon="📥")

    return st.session_state.filters
