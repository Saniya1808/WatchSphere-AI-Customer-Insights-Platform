"""
WatchSphere AI v3.0 - Phase 5 Real Data Verification Test Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import os
import sys
from pathlib import Path
import pytest
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
from frontend.utils.api_client import APIClient


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_primary_smartwatch_dataset_properties():
    """Verify primary smartwatch dataset products.csv properties."""
    csv_path = PROJECT_ROOT / "datasets" / "products.csv"
    assert csv_path.exists()

    df = pd.read_csv(csv_path)
    assert len(df) == 1000
    assert len(df.columns) >= 10
    assert "ProductID" in df.columns
    assert "ProductName" in df.columns
    assert "Price" in df.columns


def test_database_table_record_counts():
    """Verify database records created for each SQLAlchemy model."""
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


def test_api_client_kpi_consistency():
    """Verify APIClient returns consistent dynamic KPIs from database/REST."""
    kpis = APIClient.get_dashboard_kpis()
    assert kpis["total_orders"]["numeric_value"] == 8000
    assert kpis["total_customers"]["numeric_value"] == 3000
    assert kpis["total_products"]["numeric_value"] == 1000
    assert kpis["total_vendors"]["numeric_value"] >= 12
    assert kpis["total_revenue"]["numeric_value"] > 0
