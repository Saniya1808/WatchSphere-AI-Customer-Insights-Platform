"""
WatchSphere AI v3.0 - Customer Segmentation AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from config.database import SessionLocal
from backend.services.customer_service import CustomerService
from ml.customer_segmentation import CustomerSegmentationEngine


def render_ai_segmentation_tab() -> None:
    """
    Renders Customer Segmentation tab with KMeans Elbow Curve, 2D/3D PCA plots, and Personas.
    """
    db = SessionLocal()
    try:
        cust_service = CustomerService(db)
        customers = cust_service.get_all()
        df_cust = pd.DataFrame([{"full_name": c.full_name, "age": c.age, "orders_count": c.orders_count, "total_spending": c.total_spending, "recency_days": 15} for c in customers]) if customers else pd.DataFrame()

        # Controls & KPI
        c_k, c_sil = st.columns([3, 1])
        with c_k:
            k_val = st.slider("Select Cluster Count (K)", min_value=2, max_value=6, value=4, key="seg_k_slider")
        
        seg_res = CustomerSegmentationEngine.run_segmentation(df_cust, n_clusters=k_val)
        with c_sil:
            st.markdown(
                f"""
                <div class="ws-glass-card" style="padding: 12px; text-align: center;">
                    <div style="font-size: 0.85rem; color: var(--text-sub);">Silhouette Score</div>
                    <div style="font-size: 1.6rem; font-weight: 700; color: #10B981;">{seg_res['silhouette_score']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 2D & 3D PCA Scatter Plots
        col1, col2 = st.columns(2)
        df_seg = seg_res["df_segmented"]

        with col1:
            fig_2d = px.scatter(df_seg, x="pca_x", y="pca_y", color="persona", hover_data=["full_name", "total_spending"], title="📍 2D PCA Customer Cluster Map")
            fig_2d.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
            st.plotly_chart(fig_2d, use_container_width=True)

        with col2:
            fig_3d = px.scatter_3d(df_seg, x="pca_x", y="pca_y", z="pca_z", color="persona", hover_data=["full_name"], title="🌐 3D PCA Cluster Space")
            fig_3d.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
            st.plotly_chart(fig_3d, use_container_width=True)

        # Elbow Curve Chart
        df_elbow = pd.DataFrame(seg_res["elbow_data"])
        fig_el = px.line(df_elbow, x="k", y="inertia", markers=True, title="📉 KMeans Optimal K (Elbow Method Curve)", color_discrete_sequence=["#6366F1"])
        fig_el.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig_el, use_container_width=True)

        # Cluster Table
        st.markdown("### 👥 Customer Cluster Assignments Directory")
        st.dataframe(df_seg[["full_name", "orders_count", "total_spending", "persona"]], use_container_width=True)

    finally:
        db.close()
