"""
WatchSphere AI v3.0 - Sentiment Analysis AI Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from ml.sentiment_analysis import SentimentAnalysisEngine

COLOR_SEQ = ["#10B981", "#0EA5E9", "#F43F5E"]


def render_ai_sentiment_tab() -> None:
    """
    Renders Sentiment Analysis tab with real-time text classifier, sentiment distribution pie, and keywords.
    """
    st.markdown("### 💬 Real-Time Review Sentiment Analyzer")

    sample_text = st.text_area("Input Customer Review Text", value="The build quality of this WatchSphere Pro watch is absolute perfection! Superb battery life and fast delivery.", key="sentiment_input_area")

    if st.button("Analyze Sentiment", type="primary", key="btn_run_sentiment"):
        res = SentimentAnalysisEngine.analyze_text(sample_text)
        badge_color = "#10B981" if res["sentiment"] == "Positive" else ("#F43F5E" if res["sentiment"] == "Negative" else "#0EA5E9")

        st.markdown(
            f"""
            <div class="ws-glass-card" style="padding: 20px; border-left: 5px solid {badge_color}; margin-top: 15px;">
                <h3 style="margin: 0 0 8px 0; color: {badge_color};">
                    Predicted Sentiment: {res['sentiment'].upper()}
                </h3>
                <p style="margin: 0; font-size: 1.1rem; color: var(--text-sub);">
                    Confidence Certainty: <strong>{res['confidence']*100:.1f}%</strong> | Score: <strong>{res['score']}</strong>
                </p>
                <p style="margin-top: 8px; color: var(--text-sub);">
                    Extracted Keywords: <strong>{', '.join(res['keywords']) if res['keywords'] else 'N/A'}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Sentiment Distribution Pie Chart
    col1, col2 = st.columns(2)
    with col1:
        df_sent = pd.DataFrame({
            "sentiment": ["Positive", "Neutral", "Negative"],
            "count": [142, 28, 12]
        })
        fig = px.pie(df_sent, names="sentiment", values="count", title="📊 Review Sentiment Breakdown", color_discrete_sequence=COLOR_SEQ, hole=0.4)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_words = pd.DataFrame({
            "keyword": ["perfection", "quality", "battery", "fast", "terrible", "defective"],
            "frequency": [85, 78, 64, 52, 14, 8]
        })
        fig_w = px.bar(df_words, x="frequency", y="keyword", orientation="h", title="🔤 Top Extracted Sentiment Keywords", color_discrete_sequence=["#6366F1"])
        fig_w.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
        st.plotly_chart(fig_w, use_container_width=True)
