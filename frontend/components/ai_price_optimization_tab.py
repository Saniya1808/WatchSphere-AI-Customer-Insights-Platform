"""
WatchSphere AI v3.0 - Price Optimization AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from ml.price_optimization import PriceOptimizationEngine
from frontend.components.cards import render_metric_card


def render_ai_price_optimization_tab() -> None:
    """
    Renders Price Optimization tab with price elasticity profit curves and recommended prices.
    """
    st.markdown("### 🏷️ Dynamic Price & Profit Margin Optimization")

    col1, col2 = st.columns(2)
    with col1:
        cost_p = st.number_input("Cost Price ($)", min_value=10.0, value=350.0, key="price_cost_input")
    with col2:
        curr_p = st.number_input("Current Selling Price ($)", min_value=10.0, value=799.0, key="price_curr_input")

    res = PriceOptimizationEngine.optimize_price(cost_p, curr_p)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Current Price", f"${curr_p:.2f}", "Baseline Selling Price", "Catalog")
    with c2:
        render_metric_card("Suggested Price", f"${res['suggested_price']:.2f}", "AI Optimal Price", "Active")
    with c3:
        render_metric_card("Expected Profit", f"${res['expected_profit']:,.2f}", "Maximization Peak", "Revenue")
    with c4:
        render_metric_card("Profit Lift", f"+{res['profit_lift_pct']}%", "Margin Gain", "Success")

    st.markdown("<br>", unsafe_allow_html=True)

    # Elasticity Profit Curve Chart
    df_curve = res["curve_df"]
    fig = px.line(df_curve, x="price", y="expected_profit", title="📈 Price vs Expected Profit Elasticity Curve", markers=True, color_discrete_sequence=["#10B981"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
    st.plotly_chart(fig, use_container_width=True)
