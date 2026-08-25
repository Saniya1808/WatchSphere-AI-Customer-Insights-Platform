"""
WatchSphere AI v3.0 - Artificial Intelligence & Machine Learning Studio (Phase 6)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.utils.session import SessionManager
from frontend.components.footer import render_footer
from frontend.components.ai_dashboard_tab import render_ai_dashboard_tab
from frontend.components.ai_segmentation_tab import render_ai_segmentation_tab
from frontend.components.ai_recommendation_tab import render_ai_recommendation_tab
from frontend.components.ai_sentiment_tab import render_ai_sentiment_tab
from frontend.components.ai_sales_forecast_tab import render_ai_sales_forecast_tab
from frontend.components.ai_demand_forecast_tab import render_ai_demand_forecast_tab
from frontend.components.ai_churn_tab import render_ai_churn_tab
from frontend.components.ai_price_optimization_tab import render_ai_price_optimization_tab
from frontend.components.ai_fraud_tab import render_ai_fraud_tab
from frontend.components.ai_model_center_tab import render_ai_model_center_tab


def render_ai_engine_page() -> None:
    """
    Renders the complete Enterprise AI & Machine Learning Studio with 10 Tabs:
    1. AI Dashboard
    2. Customer Segmentation
    3. Recommendation Engine
    4. Sentiment Analysis
    5. Sales Forecasting
    6. Demand Forecasting
    7. Churn Prediction
    8. Price Optimization
    9. Fraud Detection
    10. AI Model Center

    Enforces Role-Based Access Scoping for Admin vs Vendor users.
    """
    user_role = (SessionManager.get_user_role() or "").lower()

    st.markdown(
        f"""
        <div class="ws-breadcrumb">
            Home / <span>Artificial Intelligence</span>
        </div>
        <div style="margin-bottom: 16px;">
            <h1 style="font-family: var(--font-heading); font-size: 2.2rem; margin: 0; color: var(--text-main);">
                Artificial Intelligence & Machine Learning Studio
            </h1>
            <p style="color: var(--accent-indigo); font-size: 1rem; font-weight: 600; margin: 4px 0 0 0;">
                Predictive Analytics, Segmentation, Forecasting & NLP Sentiment Engine
                <span class="ws-badge ws-badge-brand" style="margin-left: 10px;">{user_role.upper()} PORTAL</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if user_role == "admin":
        tab_titles = [
            "🤖 1. AI Dashboard",
            "🧩 2. Segmentation",
            "🎯 3. Recommender",
            "💬 4. Sentiment NLP",
            "📈 5. Sales Forecast",
            "📦 6. Demand Forecast",
            "⚠️ 7. Churn Risk",
            "🏷️ 8. Price Optimal",
            "🚨 9. Fraud Detection",
            "⚙️ 10. Model Center"
        ]
    else:  # Vendor Scoped View
        tab_titles = [
            "🎯 1. Product Recommendations",
            "📈 2. Product Sales Forecast",
            "📦 3. Stock Demand Forecast",
            "💬 4. Review Sentiment NLP"
        ]

    tabs = st.tabs(tab_titles)

    if user_role == "admin":
        with tabs[0]:
            render_ai_dashboard_tab()
        with tabs[1]:
            render_ai_segmentation_tab()
        with tabs[2]:
            render_ai_recommendation_tab()
        with tabs[3]:
            render_ai_sentiment_tab()
        with tabs[4]:
            render_ai_sales_forecast_tab()
        with tabs[5]:
            render_ai_demand_forecast_tab()
        with tabs[6]:
            render_ai_churn_tab()
        with tabs[7]:
            render_ai_price_optimization_tab()
        with tabs[8]:
            render_ai_fraud_tab()
        with tabs[9]:
            render_ai_model_center_tab()
    else:
        # Vendor Scoped Tabs
        with tabs[0]:
            render_ai_recommendation_tab()
        with tabs[1]:
            render_ai_sales_forecast_tab()
        with tabs[2]:
            render_ai_demand_forecast_tab()
        with tabs[3]:
            render_ai_sentiment_tab()

    render_footer()
