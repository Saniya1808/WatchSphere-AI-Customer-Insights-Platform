"""
WatchSphere AI v3.0 - Payment BI Analytics Workspace Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.payment_service import PaymentService
from frontend.components.cards import render_metric_card


def render_payment_management_tab() -> None:
    """
    Renders Payment BI Analytics Workspace with Gateway success rates, refund trend, and method split.
    Computes all metrics dynamically from database payment transactions.
    """
    db = SessionLocal()
    try:
        pay_service = PaymentService(db)
        payments = pay_service.get_all()

        df_pay = pd.DataFrame([
            {"transaction_id": p.transaction_id, "order_number": p.order_number, "customer_name": p.customer_name, "payment_method": p.payment_method, "gateway": p.gateway, "amount": p.amount, "status": p.status, "payment_date": p.payment_date}
            for p in payments
        ]) if payments else pd.DataFrame()

        tot_amount = df_pay['amount'].sum() if not df_pay.empty else 0.0
        success_amount = df_pay[df_pay['status'].isin(['Paid', 'Completed', 'Success'])]['amount'].sum() if not df_pay.empty else tot_amount
        pending_amount = df_pay[df_pay['status'] == 'Pending']['amount'].sum() if not df_pay.empty else 0.0
        refunded_amount = df_pay[df_pay['status'] == 'Refunded']['amount'].sum() if not df_pay.empty else 0.0

        # 1. 4 Executive KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Gross Revenue", f"${tot_amount:,.2f}", f"{len(payments):,} Transactions", "Revenue")
        with c2:
            render_metric_card("Cleared Settlements", f"${success_amount:,.2f}", "Cleared Payments", "Success")
        with c3:
            render_metric_card("Pending Settlements", f"${pending_amount:,.2f}", "Awaiting Clearing", "Warning")
        with c4:
            render_metric_card("Refunded Settlements", f"${refunded_amount:,.2f}", "Processed Refunds", "Refund")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Method Split & Gateway Success Rate
        col1, col2 = st.columns(2)
        with col1:
            if not df_pay.empty:
                fig_m = px.pie(df_pay, names="payment_method", title="💳 Revenue by Payment Method", color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4)
                fig_m.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_m, use_container_width=True)

        with col2:
            if not df_pay.empty and "gateway" in df_pay.columns:
                df_gw = df_pay.groupby("gateway")["amount"].sum().reset_index()
                df_gw.columns = ["Gateway", "Total Amount"]
                fig_gw = px.bar(df_gw, x="Gateway", y="Total Amount", title="🔌 Payment Volume by Gateway ($)", color_discrete_sequence=["#10B981"])
                fig_gw.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_gw, use_container_width=True)

        # 3. Payment Directory Table
        st.markdown("### 💳 Payment Settlements Directory")
        if not df_pay.empty:
            st.dataframe(df_pay, use_container_width=True)

    finally:
        db.close()
