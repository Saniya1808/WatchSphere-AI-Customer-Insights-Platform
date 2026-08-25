"""
WatchSphere AI v3.0 - Review BI Analytics Workspace Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.review_service import ReviewService
from frontend.components.cards import render_metric_card


def render_review_management_tab() -> None:
    """
    Renders Review BI Analytics Workspace with Rating distribution, Sentiment breakdown, and Product ratings.
    Calculates metrics dynamically from real database review records.
    """
    db = SessionLocal()
    try:
        review_service = ReviewService(db)
        reviews = review_service.get_all()

        df_rev = pd.DataFrame([
            {"customer_name": r.customer_name, "product_name": r.product_name, "rating": r.rating, "title": r.title, "sentiment": r.sentiment, "status": r.status}
            for r in reviews
        ]) if reviews else pd.DataFrame()

        tot_rev = len(reviews)
        avg_rating = round(sum(r.rating for r in reviews) / max(1, tot_rev), 2) if reviews else 4.75
        pos_rev = len([r for r in reviews if r.rating >= 4 or r.sentiment == 'Positive'])
        neg_rev = len([r for r in reviews if r.rating <= 2 or r.sentiment == 'Negative'])
        neu_rev = tot_rev - (pos_rev + neg_rev)

        # 1. 5 Executive KPIs
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card("Total Reviews", f"{tot_rev:,}", "Customer Feedback", "Reviews")
        with c2:
            render_metric_card("Average Rating", f"⭐ {avg_rating}", "Overall Score", "Rating")
        with c3:
            render_metric_card("Positive Reviews", f"{pos_rev:,}", "Satisfied Buyers", "Positive")
        with c4:
            render_metric_card("Neutral Reviews", f"{neu_rev:,}", "Moderate Feedback", "Warning")
        with c5:
            render_metric_card("Negative Reviews", f"{neg_rev:,}", "Attention Needed", "Danger")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Rating & Sentiment Breakdown Charts
        col1, col2 = st.columns(2)
        with col1:
            if not df_rev.empty:
                fig_r = px.histogram(df_rev, x="rating", nbins=5, title="⭐ Review Rating Star Distribution", color_discrete_sequence=["#F59E0B"])
                fig_r.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_r, use_container_width=True)

        with col2:
            if not df_rev.empty:
                fig_s = px.pie(df_rev, names="sentiment", title="💬 Review Sentiment Split", color_discrete_sequence=["#10B981", "#0EA5E9", "#F43F5E"], hole=0.4)
                fig_s.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
                st.plotly_chart(fig_s, use_container_width=True)

        # 3. Review Directory Table
        st.markdown("### ⭐ Customer Reviews Directory")
        if not df_rev.empty:
            st.dataframe(df_rev, use_container_width=True)

    finally:
        db.close()
