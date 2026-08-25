"""
WatchSphere AI v3.0 - Executive Analytics & BI Unit Tests (Phase 3)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import pandas as pd
from backend.services.dataset_manager import DatasetManager
from backend.services.file_validation_service import FileValidationService
from backend.services.kpi_engine import KPIEngine
from backend.services.filter_engine import FilterEngine
from backend.services.analytics_service import AnalyticsService
from backend.services.dashboard_service import DashboardService


def test_dataset_manager_status():
    """Verify DatasetManager scans datasets directory and returns status metadata."""
    statuses = DatasetManager.get_all_dataset_status()
    assert len(statuses) == 22
    assert any(d["dataset_name"] == "Orders" for d in statuses)


def test_file_validation_service():
    """Verify DataFrame schema validation logic."""
    df_sample = pd.DataFrame({
        "order_id": ["ORD-001", "ORD-002", "ORD-001"],
        "total_revenue": [100.0, 200.0, 100.0]
    })
    valid, warnings, summary = FileValidationService.validate_dataframe(df_sample, "Orders")
    assert valid is True
    assert summary["duplicate_rows"] == 1
    assert any("duplicate" in w.lower() for w in warnings)


def test_kpi_engine_calculation():
    """Verify 12 KPI calculation metrics."""
    df_orders = pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2"],
        "total_revenue": [500.0, 1500.0],
        "customer_id": ["CUST-1", "CUST-2"],
        "vendor_name": ["VEND-1", "VEND-2"]
    })
    df_products = pd.DataFrame({"stock": [10, 20]})
    df_customers = pd.DataFrame({"customer_id": ["CUST-1", "CUST-2"]})
    df_vendors = pd.DataFrame({"vendor_id": ["VEND-1", "VEND-2"]})
    df_inventory = pd.DataFrame({"inventory_value": [10000.0]})
    df_reviews = pd.DataFrame({"rating": [5.0, 4.0]})

    kpis = KPIEngine.calculate_all_kpis(
        df_orders, df_products, df_customers, df_vendors, df_inventory, df_reviews
    )

    assert "total_revenue" in kpis
    assert kpis["total_revenue"]["value"] == "$2,000.00"
    assert kpis["total_orders"]["value"] == "2"
    assert len(kpis) == 12


def test_filter_engine():
    """Verify multi-dimensional filter engine filtering logic."""
    df_orders = pd.DataFrame({
        "vendor_name": ["Acme Watch Co.", "Swiss TimeCraft"],
        "category": ["Smartwatches", "Luxury Watches"],
        "total_revenue": [500.0, 1500.0]
    })
    filters = {"vendor": "Acme Watch Co.", "category": "All Categories"}
    filtered_df = FilterEngine.apply_filters(df_orders, filters)
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]["vendor_name"] == "Acme Watch Co."


def test_dashboard_service_alerts_and_summary():
    """Verify real-time alert center and AI executive summary outputs."""
    alerts = DashboardService.get_realtime_alerts()
    assert len(alerts) == 8
    
    ai_summary = DashboardService.get_ai_executive_summary()
    assert len(ai_summary["insights"]) >= 5
    assert len(ai_summary["suggested_actions"]) >= 3
