"""
WatchSphere AI v3.0 - Phase 8 Real Data Analytics, KPI Accuracy & Database Verification Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import sys
from pathlib import Path
import pytest
from sqlalchemy import func
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import SessionLocal, engine, Base
from datasets.seed_datasets import auto_seed_datasets
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.models.product import Product
from backend.models.customer import Customer
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.payment import Payment
from backend.models.review import Review
from backend.models.wishlist import Wishlist
from backend.models.product_image import ProductImage
from backend.services.kpi_engine import KPIEngine
from backend.services.dashboard_service import DashboardService
from frontend.utils.api_client import APIClient


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_database_record_count_parity():
    """Verify database record counts for all 11 core models."""
    db = SessionLocal()
    try:
        assert db.query(Vendor).count() >= 12
        assert db.query(Category).count() == 3
        assert db.query(Subcategory).count() == 15
        assert db.query(Product).count() == 1000
        assert db.query(Customer).count() == 3000
        assert db.query(Order).count() == 8000
        assert db.query(OrderItem).count() == 16015
        assert db.query(Payment).count() == 8000
        assert db.query(Review).count() == 5000
        assert db.query(Wishlist).count() == 4000
        assert db.query(ProductImage).count() == 1000
    finally:
        db.close()


def test_kpi_mathematical_accuracy():
    """Verify aggregated KPI metrics calculated directly from SQLite database."""
    db = SessionLocal()
    try:
        tot_rev = db.query(func.sum(Order.total_amount)).scalar() or 0.0
        tot_orders = db.query(func.count(Order.id)).scalar()
        tot_custs = db.query(func.count(Customer.id)).scalar()
        tot_prods = db.query(func.count(Product.id)).scalar()
        tot_vends = db.query(func.count(Vendor.id)).scalar()
        avg_rating = db.query(func.avg(Review.rating)).scalar() or 0.0

        assert tot_orders == 8000
        assert tot_custs == 3000
        assert tot_prods == 1000
        assert tot_vends >= 12
        assert float(tot_rev) > 4000000.0
        assert float(avg_rating) >= 4.0
    finally:
        db.close()


def test_dashboard_service_and_api_client_parity():
    """Verify APIClient and direct database query return identical KPI results."""
    db = SessionLocal()
    try:
        tot_orders_db = db.query(func.count(Order.id)).scalar()
        tot_custs_db = db.query(func.count(Customer.id)).scalar()
        tot_prods_db = db.query(func.count(Product.id)).scalar()

        client_kpis = APIClient.get_dashboard_kpis()

        assert client_kpis["total_orders"]["numeric_value"] == tot_orders_db == 8000
        assert client_kpis["total_customers"]["numeric_value"] == tot_custs_db == 3000
        assert client_kpis["total_products"]["numeric_value"] == tot_prods_db == 1000
        assert client_kpis["total_revenue"]["numeric_value"] > 0
    finally:
        db.close()


def test_kpi_engine_dataframe_calculation():
    """Verify KPIEngine calculates KPIs from dataset DataFrames matching database totals."""
    datasets_dir = PROJECT_ROOT / "datasets"
    df_orders = pd.read_csv(datasets_dir / "orders.csv")
    df_products = pd.read_csv(datasets_dir / "products.csv")
    df_customers = pd.read_csv(datasets_dir / "customers.csv")
    df_vendors = pd.read_csv(datasets_dir / "vendors.csv")
    df_inventory = pd.read_csv(datasets_dir / "inventory.csv")
    df_reviews = pd.read_csv(datasets_dir / "reviews.csv")

    kpis = KPIEngine.calculate_all_kpis(
        df_orders=df_orders,
        df_products=df_products,
        df_customers=df_customers,
        df_vendors=df_vendors,
        df_inventory=df_inventory,
        df_reviews=df_reviews
    )

    assert kpis["total_orders"]["value"] == "8,000"
    assert kpis["total_customers"]["value"] == "3,000"
    assert kpis["total_products"]["value"] == "1000"
    assert kpis["total_vendors"]["value"] == "12"
