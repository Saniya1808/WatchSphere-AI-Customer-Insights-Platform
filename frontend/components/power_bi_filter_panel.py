"""
WatchSphere AI v3.0 - Power BI Style Slicer & Filter Panel Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from typing import Dict, Any
from config.database import SessionLocal
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.customer import Customer
from backend.models.order import Order


def render_power_bi_filter_panel() -> Dict[str, Any]:
    """
    Renders Power BI Slicer Panel allowing cross-filtering by Date, Vendor, Category, Customer, Region, Status.
    Options dynamically queried from database.
    """
    db = SessionLocal()
    try:
        vendors = [v.company_name for v in db.query(Vendor.company_name).distinct().all() if v.company_name]
        categories = [c.name for c in db.query(Category.name).distinct().all() if c.name]
        regions = [c[0] for c in db.query(Customer.city).distinct().all() if c[0]]
        statuses = [s[0] for s in db.query(Order.order_status).distinct().all() if s[0]]
    except Exception:
        vendors = []
        categories = []
        regions = []
        statuses = []
    finally:
        db.close()

    vendor_opts = ["All Vendors"] + sorted(vendors)
    cat_opts = ["All Categories"] + sorted(categories)
    region_opts = ["All Regions"] + sorted(regions)
    status_opts = ["All Statuses"] + sorted(statuses)

    with st.expander("🎛️ Power BI Executive Slicers & Dynamic Filter Panel", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            date_range = st.date_input("Date Range", value=[], key="pbi_filter_date_range")
            vendor_f = st.selectbox("Vendor Slicer", options=vendor_opts, key="pbi_filter_vendor")
        with c2:
            cat_f = st.selectbox("Category Slicer", options=cat_opts, key="pbi_filter_category")
            region_f = st.selectbox("Region Slicer", options=region_opts, key="pbi_filter_region")
        with c3:
            status_f = st.selectbox("Order Status Slicer", options=status_opts, key="pbi_filter_status")
            pmt_f = st.selectbox("Payment Slicer", options=["All Methods", "Credit Card", "UPI", "Debit Card", "Net Banking", "Wallet", "COD"], key="pbi_filter_payment")
        with c4:
            wh_f = st.selectbox("Warehouse Slicer", options=["All Warehouses", "WH-East Coast", "WH-West Coast", "WH-Europe Hub", "WH-Asia Pacific"], key="pbi_filter_wh")
            gender_f = st.selectbox("Gender Slicer", options=["All Genders", "Male", "Female", "Unspecified"], key="pbi_filter_gender")

    return {
        "date_range": date_range,
        "vendor": vendor_f,
        "category": cat_f,
        "region": region_f,
        "status": status_f,
        "payment_method": pmt_f,
        "warehouse": wh_f,
        "gender": gender_f
    }
