"""
WatchSphere AI v3.0 - Reports Center Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.reporting_service import ReportingService
from backend.services.order_service import OrderService
from backend.services.product_service import ProductService
from backend.services.customer_service import CustomerService
from backend.services.vendor_service import VendorService


def render_reports_center_tab() -> None:
    """
    Renders Reports Center tab with 13 domain report options, format selectors (PDF, Excel, CSV, HTML), and downloads.
    Fetches real database records dynamically for report generation.
    """
    db = SessionLocal()
    try:
        st.markdown("### 📄 Enterprise Reports Generator Center")

        r_col1, r_col2, r_col3 = st.columns([2, 1, 1])
        with r_col1:
            sel_domain = st.selectbox("Select Report Domain", options=ReportingService.REPORT_DOMAINS, key="report_domain_select")
        with r_col2:
            sel_format = st.selectbox("Export Format", options=["PDF", "Excel", "CSV", "HTML"], key="report_format_select")
        with r_col3:
            st.markdown("<br>", unsafe_allow_html=True)
            btn_gen = st.button("⚡ Generate Report", type="primary", key="btn_exec_gen_report", use_container_width=True)

        if "sales" in sel_domain.lower() or "revenue" in sel_domain.lower():
            orders = OrderService(db).get_all()
            report_data = [{"OrderNumber": o.order_number, "Customer": o.customer_name, "Vendor": o.vendor_name, "Amount": o.total_amount, "Status": o.order_status, "Date": o.order_date} for o in orders[:500]]
        elif "product" in sel_domain.lower() or "inventory" in sel_domain.lower():
            products = ProductService(db).get_all()
            report_data = [{"SKU": p.sku, "Name": p.name, "Brand": p.brand, "Category": p.category_name, "Price": p.selling_price, "Stock": p.current_stock} for p in products]
        elif "customer" in sel_domain.lower():
            customers = CustomerService(db).get_all()
            report_data = [{"Name": c.full_name, "Email": c.email, "Phone": c.phone, "City": c.city, "Segment": c.segment, "Spending": c.total_spending} for c in customers]
        elif "vendor" in sel_domain.lower():
            vendors = VendorService(db).get_all()
            report_data = [{"Company": v.company_name, "Owner": v.owner_name, "Email": v.email, "Phone": v.phone, "City": v.city, "Status": v.status} for v in vendors]
        else:
            orders = OrderService(db).get_all()
            report_data = [{"OrderNumber": o.order_number, "Customer": o.customer_name, "Vendor": o.vendor_name, "Amount": o.total_amount, "Status": o.order_status, "Date": o.order_date} for o in orders[:100]]

        if btn_gen or st.session_state.get("last_generated_report"):
            st.session_state.last_generated_report = True
            payload, filename = ReportingService.generate_report_bytes(sel_domain, sel_format, report_data)

            st.success(f"Generated `{filename}` with {len(report_data):,} real records successfully!")
            mime_type = "text/csv" if sel_format == "CSV" else ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if sel_format == "Excel" else ("text/html" if sel_format == "HTML" else "application/pdf"))
            st.download_button(f"📥 Download {sel_domain} ({sel_format})", data=payload, file_name=filename, mime=mime_type)

            st.markdown("#### 👁️ Generated Report Preview")
            st.dataframe(pd.DataFrame(report_data).head(50), use_container_width=True)

    finally:
        db.close()
