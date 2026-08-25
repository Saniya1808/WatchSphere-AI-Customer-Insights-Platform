"""
WatchSphere AI v3.0 - Commerce Power BI Analytics Unit Tests
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import pandas as pd
from backend.services.commerce_bi_analytics_service import CommerceBIAnalyticsService


def test_rfm_segmentation():
    """Test RFM Customer Segmentation Calculation."""
    df_cust = pd.DataFrame([
        {"full_name": "Cust A", "recency_days": 2, "orders_count": 20, "total_spending": 5000.0},
        {"full_name": "Cust B", "recency_days": 15, "orders_count": 5, "total_spending": 1500.0},
        {"full_name": "Cust C", "recency_days": 80, "orders_count": 1, "total_spending": 100.0}
    ])
    df_rfm = CommerceBIAnalyticsService.get_rfm_segmentation(df_cust)
    assert "rfm_segment" in df_rfm.columns
    assert len(df_rfm) == 3


def test_abc_xyz_analysis():
    """Test ABC / XYZ Inventory Categorization."""
    df_prd = pd.DataFrame([
        {"sku": "SKU-1", "name": "Prod 1", "selling_price": 1000.0, "current_stock": 50},
        {"sku": "SKU-2", "name": "Prod 2", "selling_price": 200.0, "current_stock": 10}
    ])
    df_abc = CommerceBIAnalyticsService.get_abc_xyz_analysis(df_prd)
    assert "abc_category" in df_abc.columns
    assert "xyz_volatility" in df_abc.columns


def test_waterfall_profit_data():
    """Test Waterfall Profit Bridge Calculation."""
    data = CommerceBIAnalyticsService.get_waterfall_profit_data(100000.0)
    assert len(data) == 6
    assert data[0]["amount"] == 100000.0


def test_pareto_revenue_data():
    """Test Pareto 80/20 Revenue Contribution."""
    df_prd = pd.DataFrame([
        {"name": "Item A", "revenue": 8000.0},
        {"name": "Item B", "revenue": 2000.0}
    ])
    df_par = CommerceBIAnalyticsService.get_pareto_revenue_data(df_prd)
    assert "cum_pct" in df_par.columns
    assert df_par["cum_pct"].iloc[0] == 80.0


def test_sankey_data():
    """Test Sankey Diagram node-link structure."""
    sankey = CommerceBIAnalyticsService.get_sankey_data()
    assert "labels" in sankey
    assert "source" in sankey
    assert "target" in sankey
    assert "value" in sankey
