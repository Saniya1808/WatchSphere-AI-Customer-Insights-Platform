"""
WatchSphere AI v3.0 - Recommendation Engine AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.product_service import ProductService
from ml.recommendation_engine import HybridRecommendationEngine
from frontend.components.cards import render_metric_card


def render_ai_recommendation_tab() -> None:
    """
    Renders Recommendation Engine tab with top product recommendations and Precision@K evaluation metrics.
    """
    db = SessionLocal()
    try:
        prd_service = ProductService(db)
        products = prd_service.get_all()
        df_prd = pd.DataFrame([{"sku": p.sku, "name": p.name, "brand": p.brand, "category_name": p.category_name, "selling_price": p.selling_price} for p in products]) if products else pd.DataFrame()

        # Target Product Select
        col_sel, col_empty = st.columns([2, 2])
        with col_sel:
            target_sku = st.selectbox("Select Seed Product for Recommendations", options=[p.sku for p in products] if products else ["SKU-001"], key="rec_seed_select")

        rec_res = HybridRecommendationEngine.get_recommendations(target_sku, df_prd)
        metrics = rec_res["metrics"]

        # Evaluation Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Precision@K", f"{metrics['precision_at_k']*100:.1f}%", "Recommendation Accuracy", "Success")
        with c2:
            render_metric_card("Recall@K", f"{metrics['recall_at_k']*100:.1f}%", "Relevant Item Coverage", "Active")
        with c3:
            render_metric_card("MAP Score", f"{metrics['map_score']*100:.1f}%", "Mean Average Precision", "VIP")
        with c4:
            render_metric_card("NDCG Score", f"{metrics['ndcg_score']*100:.1f}%", "Ranking Quality", "Rating")

        st.markdown("<br>", unsafe_allow_html=True)

        # Recommendation Results Table
        st.markdown(f"### 🤖 Recommended Products for Target `{target_sku}`")
        df_recs = pd.DataFrame(rec_res["recommendations"])
        st.dataframe(df_recs, use_container_width=True)

    finally:
        db.close()
