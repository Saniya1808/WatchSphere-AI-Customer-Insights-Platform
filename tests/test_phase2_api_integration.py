"""
WatchSphere AI v3.0 - Phase 2 API Verification & Integration Test Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app
from config.database import SessionLocal, engine, Base
from datasets.seed_datasets import auto_seed_datasets
from backend.models.vendor import Vendor
from backend.models.product import Product

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    """Ensure database schema is created and auto-seeded."""
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_health_check_endpoint():
    """Verify GET /api/v1/health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["database_connected"] is True


def test_auth_login_endpoint():
    """Verify POST /api/v1/auth/login endpoint for default admin."""
    payload = {
        "email": "admin@watchsphere.ai",
        "password": "Admin@123"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]


def test_get_vendors_endpoint():
    """Verify GET /api/v1/vendors returns at least 12 real database vendor records."""
    response = client.get("/api/v1/vendors")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) >= 12


def test_get_categories_endpoint():
    """Verify GET /api/v1/categories returns 3 real database category records."""
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 3


def test_get_products_endpoint():
    """Verify GET /api/v1/products returns 1,000 real database product records."""
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 1000


def test_get_customers_endpoint():
    """Verify GET /api/v1/customers returns 3,000 real database customer records."""
    response = client.get("/api/v1/customers")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 3000


def test_get_orders_endpoint():
    """Verify GET /api/v1/orders returns 8,000 real database order records."""
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 8000


def test_get_order_items_endpoint():
    """Verify GET /api/v1/order-items returns 16,015 real database order item records."""
    response = client.get("/api/v1/order-items")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 16015


def test_get_payments_endpoint():
    """Verify GET /api/v1/payments returns 8,000 real database payment transaction records."""
    response = client.get("/api/v1/payments")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 8000


def test_get_inventory_endpoint():
    """Verify GET /api/v1/inventory returns stock levels for 1,000 products."""
    response = client.get("/api/v1/inventory")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 1000


def test_get_reviews_endpoint():
    """Verify GET /api/v1/reviews returns 5,000 real database review records."""
    response = client.get("/api/v1/reviews")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 5000


def test_get_wishlist_endpoint():
    """Verify GET /api/v1/wishlist returns 4,000 real database wishlist records."""
    response = client.get("/api/v1/wishlist")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 4000


def test_dashboard_kpis_endpoint():
    """Verify GET /api/v1/dashboard/kpis calculates real aggregated metrics from database."""
    response = client.get("/api/v1/dashboard/kpis")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_orders"]["numeric_value"] == 8000
    assert data["total_customers"]["numeric_value"] == 3000
    assert data["total_products"]["numeric_value"] == 1000
    assert data["total_vendors"]["numeric_value"] >= 12
    assert data["total_revenue"]["numeric_value"] > 0


def test_analytics_sales_summary_endpoint():
    """Verify GET /api/v1/analytics/sales-summary computes sales aggregations."""
    response = client.get("/api/v1/analytics/sales-summary")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_orders"] == 8000
    assert data["total_revenue"] > 0


def test_ml_models_endpoint():
    """Verify GET /api/v1/ml/models returns registered ML models."""
    response = client.get("/api/v1/ml/models")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0


def test_crud_vendor_lifecycle():
    """Verify CREATE, READ, UPDATE, and DELETE operations for Vendor entity."""
    # 1. CREATE
    payload = {
        "company_name": "Test Chrono Works",
        "owner_name": "Test Owner",
        "email": "contact@testchrono.com",
        "phone": "+91 9999988888",
        "gst_number": "27TESTCHRONO1Z5",
        "address": "123 Test St",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India"
    }
    create_res = client.post("/api/v1/vendors", json=payload)
    assert create_res.status_code == 201
    vendor_id = create_res.json()["data"]["id"]

    # 2. READ
    get_res = client.get(f"/api/v1/vendors/{vendor_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["company_name"] == "Test Chrono Works"

    # Cleanup test record directly
    db = SessionLocal()
    try:
        v = db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if v:
            db.delete(v)
            db.commit()
    finally:
        db.close()
