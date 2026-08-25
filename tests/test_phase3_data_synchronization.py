"""
WatchSphere AI v3.0 - Phase 3 Data Synchronization & Integration Test Suite
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
from backend.services.kpi_engine import KPIEngine
from backend.services.product_service import ProductService
from backend.services.customer_service import CustomerService
from backend.services.order_service import OrderService


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_all_24_csv_files_present_and_valid():
    """Verify all 24 CSV files exist in datasets/ and are readable DataFrames."""
    datasets_dir = PROJECT_ROOT / "datasets"
    all_csvs = list(datasets_dir.glob("*.csv"))
    assert len(all_csvs) >= 24, f"Expected at least 24 CSV files in datasets/, found {len(all_csvs)}"

    for csv_file in all_csvs:
        df = pd.read_csv(csv_file)
        assert not df.empty or len(df.columns) > 0, f"CSV file {csv_file.name} must contain data or valid headers"


def test_database_record_synchronization():
    """Verify core database table row counts match CSV dataset row counts."""
    db = SessionLocal()
    try:
        datasets_dir = PROJECT_ROOT / "datasets"

        mappings = [
            (Vendor, "vendors.csv"),
            (Category, "categories.csv"),
            (Subcategory, "subcategories.csv"),
            (Product, "products.csv"),
            (Customer, "customers.csv"),
            (Order, "orders.csv"),
            (OrderItem, "order_items.csv"),
            (Payment, "payments.csv"),
            (Review, "reviews.csv"),
            (Wishlist, "wishlist.csv"),
            (ProductImage, "product_images.csv")
        ]

        for model, csv_name in mappings:
            db_cnt = db.query(model).count()
            csv_cnt = len(pd.read_csv(datasets_dir / csv_name))
            if model == Vendor:
                assert db_cnt >= csv_cnt, f"Mismatch for {model.__tablename__}: DB={db_cnt}, CSV={csv_cnt}"
            else:
                assert db_cnt == csv_cnt, f"Mismatch for {model.__tablename__}: DB={db_cnt}, CSV={csv_cnt}"
    finally:
        db.close()


def test_dynamic_kpi_engine_calculation():
    """Verify KPIEngine calculates metrics from real populated database DataFrames."""
    db = SessionLocal()
    try:
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
        assert "$" in kpis["total_revenue"]["value"]
    finally:
        db.close()


def test_real_database_filtering():
    """Verify dynamic filtering over products and orders using real database services."""
    db = SessionLocal()
    try:
        prd_service = ProductService(db)
        ord_service = OrderService(db)

        # 1. Product Category Filter
        smartwatches = prd_service.get_all(category="Smart Watch")
        assert len(smartwatches) > 0
        for p in smartwatches:
            assert p.category_name == "Smart Watch"

        # 2. Order Status Filter
        delivered_orders = ord_service.get_all(order_status="Delivered")
        assert len(delivered_orders) > 0
        for o in delivered_orders:
            assert o.order_status == "Delivered"
    finally:
        db.close()
