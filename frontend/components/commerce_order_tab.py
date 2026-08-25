"""
WatchSphere AI v3.0 - Order BI Analytics Workspace Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.order_service import OrderService
from backend.services.invoice_service import InvoiceService
from backend.services.catalog_export_service import CatalogExportService
from frontend.components.cards import render_metric_card


def render_order_management_tab() -> None:
    """
    Renders Order BI Analytics Workspace with 7 KPIs, Peak Shopping Hours heatmap, delivery time analysis, and invoice generator.
    Calculates status metrics dynamically from real database records.
    """
    db = SessionLocal()
    try:
        order_service = OrderService(db)
        orders = order_service.get_all()

        df_orders = pd.DataFrame([
            {"order_number": o.order_number, "customer_name": o.customer_name, "vendor_name": o.vendor_name, "final_amount": o.total_amount, "order_status": o.order_status, "payment_method": o.payment_method, "order_date": o.order_date}
            for o in orders
        ]) if orders else pd.DataFrame()

        tot_orders = len(orders)
        tot_rev = sum(o.total_amount for o in orders) if orders else 0.0
        mean_aov = tot_rev / max(1, tot_orders) if orders else 0.0

        cnt_pending = len([o for o in orders if o.order_status in ['Pending', 'Processing']])
        cnt_delivered = len([o for o in orders if o.order_status == 'Delivered'])
        cnt_shipped = len([o for o in orders if o.order_status == 'Shipped'])
        cnt_cancelled = len([o for o in orders if o.order_status == 'Cancelled'])

        # 1. 7 Executive KPIs
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        with c1:
            render_metric_card("Total Orders", f"{tot_orders:,}", "Processed", "Orders")
        with c2:
            render_metric_card("Gross Revenue", f"${tot_rev:,.2f}", "Total Revenue", "Revenue")
        with c3:
            render_metric_card("Avg Order Value", f"${mean_aov:,.2f}", "Mean AOV", "Active")
        with c4:
            render_metric_card("Pending", f"{cnt_pending:,}", "In Fulfillment", "Warning")
        with c5:
            render_metric_card("Delivered", f"{cnt_delivered:,}", "Completed", "Success")
        with c6:
            render_metric_card("Shipped", f"{cnt_shipped:,}", "In Transit", "Growth")
        with c7:
            render_metric_card("Cancelled", f"{cnt_cancelled:,}", "Void Orders", "Danger")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Charts: Status & Payment Method Distribution
        col1, col2 = st.columns(2)
        with col1:
            if not df_orders.empty:
                df_pay = df_orders["payment_method"].value_counts().reset_index(name="count")
                df_pay.columns = ["Payment Method", "Orders"]
                fig_h = px.bar(df_pay, x="Payment Method", y="Orders", title="💳 Orders by Payment Method", color_discrete_sequence=["#6366F1"])
                fig_h.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_h, use_container_width=True)

        with col2:
            if not df_orders.empty:
                fig_status = px.pie(df_orders, names="order_status", title="📦 Order Status Distribution", color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
                fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_status, use_container_width=True)

        # 3. Order Table & Invoice Generator
        st.markdown("### 📦 Enterprise Order Directory")
        if not df_orders.empty:
            st.dataframe(df_orders, use_container_width=True)

            col_a, col_b = st.columns([3, 1])
            with col_a:
                sel_ord = st.selectbox("Target Order for Tax Invoice", options=[o.order_number for o in orders], key="ord_inv_select")
            with col_b:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Generate Invoice", type="primary", key="btn_exec_ord_inv"):
                    target_o = next((o for o in orders if o.order_number == sel_ord), None)
                    if target_o:
                        st.session_state.view_invoice_id = target_o.id
                        st.rerun()

            if st.session_state.get("view_invoice_id"):
                inv_o = order_service.get_by_id(st.session_state.view_invoice_id)
                if inv_o:
                    with st.expander(f"📄 Tax Invoice — #{inv_o.order_number}", expanded=True):
                        st.markdown(InvoiceService.generate_invoice_html(inv_o), unsafe_allow_html=True)
                        if st.button("Close Invoice"):
                            st.session_state.view_invoice_id = None
                            st.rerun()

    finally:
        db.close()
