"""
WatchSphere AI v3.0 - Multi-Format Enterprise Dataset Upload Studio Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from config.database import SessionLocal
from backend.services.etl_pipeline_service import ETLPipelineService
from frontend.components.cards import render_metric_card


def render_dataset_upload_studio() -> None:
    """
    Renders Multi-Format Enterprise Dataset Upload Studio supporting CSV, XLSX, XLS, JSON, Parquet, TSV, TXT, ZIP uploads,
    Schema Validation, Data Quality Reports, 20-Row Preview, Append/Replace modes.
    """
    db = SessionLocal()
    try:
        etl_service = ETLPipelineService(db)

        st.markdown("### 📤 Multi-Format Enterprise Dataset Upload Studio")

        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_files = st.file_uploader(
                "Drag & Drop Enterprise Dataset Files (CSV, Excel .xlsx/.xls, JSON, Parquet, TSV, TXT, ZIP)",
                type=["csv", "xlsx", "xls", "json", "parquet", "tsv", "txt", "zip"],
                accept_multiple_files=True,
                key="etl_studio_file_uploader"
            )
        with col2:
            import_mode = st.selectbox("Import Strategy", options=["Append Dataset", "Replace Dataset", "Rollback Import"], key="etl_studio_import_mode")

        if uploaded_files:
            st.markdown("#### 🔍 Batch Schema Auto-Detection & Quality Summary")

            valid_count = 0
            total_rows_ingested = 0

            for uf in uploaded_files:
                bytes_data = uf.getvalue()
                ok, msg, quality = etl_service.process_file_upload(bytes_data, uf.name, import_mode)

                if ok:
                    valid_count += 1
                    total_rows_ingested += quality.get("total_rows", 0)

                    with st.expander(f"📁 {uf.name} -> Target Schema: [{quality.get('detected_schema', 'custom').upper()}]", expanded=False):
                        st.info(f"✅ Auto-detected Schema: `{quality.get('detected_schema')}` | {quality.get('total_rows', 0):,} Rows | {quality.get('total_columns', 0)} Columns")

                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            render_metric_card("Quality Score", f"{quality.get('quality_score_pct', 100.0)}%", "Data Integrity", "Success")
                        with c2:
                            render_metric_card("Total Rows", f"{quality.get('total_rows', 0):,}", "Records Processed", "Active")
                        with c3:
                            render_metric_card("Total Columns", f"{quality.get('total_columns', 0)}", "Attributes", "Catalog")
                        with c4:
                            render_metric_card("Missing Cells", f"{quality.get('missing_cells', 0)}", "Cleaned Nulls", "Warning")

                        if "preview_df" in quality and isinstance(quality["preview_df"], pd.DataFrame):
                            st.markdown("**👁️ First 20 Rows Data Preview:**")
                            st.dataframe(quality["preview_df"], use_container_width=True)
                else:
                    st.error(msg)

            st.markdown("---")
            if st.button("🚀 Execute Fault-Tolerant ETL Ingestion & Refresh Dashboards", type="primary", key="btn_exec_etl_studio"):
                st.session_state.dataset_unlocked = True
                st.success(f"ETL Ingestion Completed! Ingested {total_rows_ingested:,} rows across {valid_count} valid files. Dashboards updated.")
                st.rerun()

    finally:
        db.close()
