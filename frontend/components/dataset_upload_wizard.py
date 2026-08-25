"""
WatchSphere AI v3.0 - 5-Step Enterprise Dataset Upload Wizard Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.etl_pipeline_service import ETLPipelineService
from frontend.components.cards import render_metric_card


def render_dataset_upload_wizard() -> None:
    """
    Renders the 5-Step Interactive Enterprise Dataset Upload Wizard:
    Step 1: File Inspection & Automatic Schema Detection
    Step 2: Data Quality Validation
    Step 3: Import Preview & Mappings
    Step 4: Append / Replace Strategy Selector
    Step 5: ETL Execution & Gateway Unlock
    """
    db = SessionLocal()
    try:
        etl_service = ETLPipelineService(db)

        st.markdown(
            """
            <div class="ws-glass-card" style="padding: 30px; margin-bottom: 25px; border-left: 5px solid #6366F1;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🧙‍♂️ Enterprise Dataset Upload Wizard</div>
                <h2 style="font-family: var(--font-heading); color: var(--text-main); margin: 0 0 8px 0;">
                    Data-Driven Platform Initialization
                </h2>
                <p style="color: var(--text-sub); font-size: 1rem; margin: 0;">
                    WatchSphere AI requires a master dataset upload to populate SQLite analytical tables before unlocking executive dashboards.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📥 Step 1 & 2: Select & Inspect Master Dataset Files")

        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_files = st.file_uploader(
                "Drag & Drop Master Dataset Files (CSV, Excel, JSON, ZIP)",
                type=["csv", "xlsx", "xls", "json", "zip"],
                accept_multiple_files=True,
                key="wizard_file_uploader"
            )
        with col2:
            import_strategy = st.selectbox("Import Strategy", options=["Append Dataset", "Replace Existing Dataset"], key="wizard_import_strategy")

        if uploaded_files:
            st.markdown("---")
            st.markdown("### 📊 Step 3 & 4: Automatic Schema Detection & Quality Inspection")

            for uf in uploaded_files:
                file_bytes = uf.getvalue()
                ok, msg, quality = etl_service.process_file_upload(file_bytes, uf.name, import_strategy)

                if ok:
                    st.success(f"✅ File `{uf.name}` -> Auto-detected Schema: `{quality.get('detected_schema', 'custom')}` ({quality.get('total_rows', 0):,} Rows)")
                    
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        render_metric_card("Quality Score", f"{quality.get('quality_score_pct', 100.0)}%", "Data Integrity", "Success")
                    with c2:
                        render_metric_card("Processed Rows", f"{quality.get('total_rows', 0):,}", "Ingested Records", "Active")
                    with c3:
                        render_metric_card("Total Columns", f"{quality.get('total_columns', 0)}", "Attributes", "Catalog")
                    with c4:
                        render_metric_card("Missing Cells", f"{quality.get('missing_cells', 0)}", "Cleaned Nulls", "Warning")

            st.markdown("---")
            st.markdown("### 🚀 Step 5: Execute ETL Ingestion & Unlock Application")

            if st.button("⚡ Ingest Dataset & Unlock Executive Platform", type="primary", key="btn_wizard_execute_etl", use_container_width=True):
                st.session_state.dataset_unlocked = True
                st.success("ETL Pipeline completed successfully! Application unlocked.")
                st.rerun()

    finally:
        db.close()
