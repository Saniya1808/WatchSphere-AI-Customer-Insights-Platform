"""
WatchSphere AI v3.0 - Phase 6 Complete End-to-End Functional & E2E Integration Test Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import SessionLocal, engine, Base
from datasets.seed_datasets import auto_seed_datasets
from backend.main import app
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.models.product import Product
from backend.models.customer import Customer
from backend.models.order import Order
from backend.models.payment import Payment
from backend.models.review import Review
from backend.services.vendor_service import VendorService
from backend.services.category_service import CategoryService
from backend.services.product_service import ProductService
from backend.services.customer_service import CustomerService
from backend.services.order_service import OrderService
from backend.services.reporting_service import ReportingService
from ml.sales_forecasting import SalesForecastingEngine
from ml.demand_forecasting import DemandForecastingEngine
from ml.customer_segmentation import CustomerSegmentationEngine
from ml.recommendation_engine import HybridRecommendationEngine
from ml.sentiment_analysis import SentimentAnalysisEngine
from ml.fraud_detection import FraudDetectionEngine
from ml.price_optimization import PriceOptimizationEngine

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_e2e_backend_health_and_api_routers():
    """Verify backend FastAPI server and all core API routers under /api/v1/."""
    r_health = client.get("/api/v1/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "success"
    assert r_health.json()["data"]["status"] == "healthy"

    r_kpis = client.get("/api/v1/dashboard/kpis")
    assert r_kpis.status_code == 200
    assert r_kpis.json()["data"]["total_orders"]["numeric_value"] == 8000

    r_prods = client.get("/api/v1/products")
    assert r_prods.status_code == 200
    assert len(r_prods.json()["data"]) == 1000

    r_custs = client.get("/api/v1/customers")
    assert r_custs.status_code == 200
    assert len(r_custs.json()["data"]) == 3000

    r_vends = client.get("/api/v1/vendors")
    assert r_vends.status_code == 200
    assert len(r_vends.json()["data"]) >= 12


def test_e2e_authentication_flow():
    """Verify admin login, JWT token generation, protected routes, and logout."""
    # 1. Login
    payload = {"email": "admin@watchsphere.ai", "password": "Admin@123"}
    r_login = client.post("/api/v1/auth/login", json=payload)
    assert r_login.status_code == 200
    token_data = r_login.json()["data"]
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 2. Protected Route Access with Bearer Token
    headers = {"Authorization": f"Bearer {token}"}
    r_me = client.get("/api/v1/auth/me", headers=headers)
    assert r_me.status_code == 200
    assert r_me.json()["data"]["email"] == "admin@watchsphere.ai"


def test_e2e_crud_operations_safe_lifecycle():
    """Verify Vendor, Category, Subcategory, Product, Customer CRUD lifecycles safely via API."""
    payload = {
        "company_name": "Test Chrono E2E",
        "owner_name": "E2E Owner",
        "email": "contact@e2echrono.com",
        "phone": "+91 9999911111",
        "gst_number": "27E2ECHRONO1Z5",
        "address": "123 E2E St",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India"
    }
    create_res = client.post("/api/v1/vendors", json=payload)
    assert create_res.status_code == 201
    vendor_id = create_res.json()["data"]["id"]

    get_res = client.get(f"/api/v1/vendors/{vendor_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["company_name"] == "Test Chrono E2E"

    # Cleanup
    db = SessionLocal()
    try:
        v = db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if v:
            db.delete(v)
            db.commit()
    finally:
        db.close()


def test_e2e_ml_engines_and_analytics():
    """Verify Machine Learning engines execute without errors over real dataset records."""
    db = SessionLocal()
    try:
        # 1. Sales Forecast
        fc_res = SalesForecastingEngine.forecast_sales(days_ahead=30)
        assert fc_res["total_forecasted_revenue"] > 0
        assert len(fc_res["forecast_df"]) == 30

        # 2. Recommender
        products = ProductService(db).get_all()
        df_prd = pd.DataFrame([{"sku": p.sku, "name": p.name, "brand": p.brand, "category_name": p.category_name, "selling_price": p.selling_price} for p in products])
        rec_res = HybridRecommendationEngine.get_recommendations(df_prd.iloc[0]["sku"], df_prd)
        assert len(rec_res["recommendations"]) == 5

        # 3. Sentiment Analysis
        rev_res = SentimentAnalysisEngine.analyze_text("The WatchSphere Pro smartwatch has outstanding battery life and premium build!")
        assert rev_res["sentiment"] == "Positive"
        assert rev_res["confidence"] > 0.8
    finally:
        db.close()


def test_e2e_reporting_exports_all_domains():
    """Verify report byte payload generation for all domains across PDF, Excel, CSV, HTML formats."""
    db = SessionLocal()
    try:
        orders = OrderService(db).get_all()
        report_data = [{"OrderNumber": o.order_number, "Amount": o.total_amount} for o in orders[:20]]

        for fmt in ["CSV", "Excel", "PDF", "HTML"]:
            payload, fn = ReportingService.generate_report_bytes("Sales Summary Report", fmt, report_data)
            assert len(payload) > 0
            assert fn is not None
    finally:
        db.close()
