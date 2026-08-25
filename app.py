"""
WatchSphere AI – Customer Insights Platform Version 3.0
AI Powered Enterprise Customer Analytics & Business Intelligence Platform
Author: Powered by Saniya Maner (Infosys Internship Project 2026)

Phase 2 Entry Point, Routing Engine & Data-Driven Gateway Guard
"""

import streamlit as st
from frontend.utils.config import init_page_config
from frontend.utils.session import SessionManager
from frontend.utils.css_loader import load_css
from frontend.layouts.landing_page import render_landing_page
from frontend.components.top_header import render_top_header
from frontend.components.sidebar import render_sidebar
from frontend.components.dataset_upload_wizard import render_dataset_upload_wizard
from frontend.pages.overview import render_overview_page
from frontend.pages.catalog import render_catalog_page
from frontend.pages.commerce import render_commerce_page
from frontend.pages.ai_engine import render_ai_engine_page
from frontend.pages.system_settings import render_system_settings_page
from config.database import SessionLocal
from backend.services.etl_pipeline_service import ETLPipelineService

# 1. Page Configuration
init_page_config()

# Master Dataset Auto Import
from datasets.seed_datasets import auto_seed_datasets
auto_seed_datasets()

# 2. Session Initialization
SessionManager.initialize_session()

# 3. CSS Injection
load_css()

# 4. Authentication Routing Security Guard
if not SessionManager.is_authenticated():
    render_landing_page()
else:
    # 5. Data-Driven Gateway Guard
    db = SessionLocal()
    try:
        etl_service = ETLPipelineService(db)
        dataset_exists = etl_service.has_imported_dataset() or st.session_state.get("dataset_unlocked", False)
    finally:
        db.close()

    if not dataset_exists:
        # Render Collapsible Sidebar
        render_sidebar()
        render_top_header()
        render_dataset_upload_wizard()
    else:
        # Render Collapsible Animated Sidebar Navigation & retrieve active page
        selected_page = render_sidebar()

        # Render Sticky Top Header
        render_top_header()

        # Authenticated Page Routing
        if selected_page == "Overview":
            render_overview_page()
        elif selected_page == "Catalog":
            render_catalog_page()
        elif selected_page == "Commerce":
            render_commerce_page()
        elif selected_page == "Artificial Intelligence":
            render_ai_engine_page()
        elif selected_page == "System Settings":
            render_system_settings_page()
        else:
            render_overview_page()
