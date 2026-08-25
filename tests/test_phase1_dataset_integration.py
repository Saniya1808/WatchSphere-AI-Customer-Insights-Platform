"""
WatchSphere AI v3.0 - Phase 1 Dataset & Database Integration Test Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import os
import sys
from pathlib import Path
import pytest
import pandas as pd

# Project root path resolution
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


@pytest.fixture(scope="module")
def db_session():
    """Initializes database schema and ensures auto_seed_datasets runs."""
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()
    db = SessionLocal()
    yield db
    db.close()


def test_csv_datasets_exist():
    """Verify all 24 expected WatchSphere CSV dataset files exist in datasets/ directory."""
    datasets_dir = PROJECT_ROOT / "datasets"
    assert datasets_dir.exists(), "datasets/ directory must exist"

    expected_csvs = [
        "cart.csv", "categories.csv", "category_sales.csv", "customer_activity.csv",
        "customers.csv", "dashboard_summary.csv", "forecast_data.csv", "inventory.csv",
        "monthly_sales.csv", "order_items.csv", "orders.csv", "payments.csv",
        "product_images.csv", "products.csv", "recommendations.csv", "reviews.csv",
        "sales_summary.csv", "subcategories.csv", "subcategory_sales.csv", "vendor_sales.csv",
        "vendors.csv", "warehouses.csv", "wishlist.csv", "yearly_sales.csv"
    ]

    for csv_file in expected_csvs:
        csv_path = datasets_dir / csv_file
        assert csv_path.exists(), f"CSV dataset file {csv_file} is missing from datasets/"


def test_database_table_counts(db_session):
    """Verify SQLite database table row counts match CSV dataset row counts 100% perfectly."""
    datasets_dir = PROJECT_ROOT / "datasets"

    entity_mapping = [
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

    for model, csv_file in entity_mapping:
        db_count = db_session.query(model).count()
        csv_df = pd.read_csv(datasets_dir / csv_file)
        csv_count = len(csv_df)
        if model == Vendor:
            assert db_count >= csv_count, f"Mismatch for {model.__tablename__}: DB={db_count}, CSV={csv_count}"
        else:
            assert db_count == csv_count, f"Mismatch for {model.__tablename__}: DB={db_count}, CSV={csv_count}"


def test_foreign_key_integrity(db_session):
    """Verify foreign key relations across imported database tables."""
    # 1. Product -> Vendor, Category, Subcategory
    products = db_session.query(Product).all()
    vendor_ids = {v.id for v in db_session.query(Vendor).all()}
    category_ids = {c.id for c in db_session.query(Category).all()}
    subcategory_ids = {sc.id for sc in db_session.query(Subcategory).all()}

    for p in products:
        assert p.vendor_id in vendor_ids, f"Product {p.id} has invalid vendor_id {p.vendor_id}"
        assert p.category_id in category_ids, f"Product {p.id} has invalid category_id {p.category_id}"
        assert p.subcategory_id in subcategory_ids, f"Product {p.id} has invalid subcategory_id {p.subcategory_id}"

    # 2. Order -> Customer
    orders = db_session.query(Order).all()
    customer_ids = {c.id for c in db_session.query(Customer).all()}
    for o in orders:
        assert o.customer_id in customer_ids, f"Order {o.id} has invalid customer_id {o.customer_id}"

    # 3. OrderItem -> Order, Product
    order_items = db_session.query(OrderItem).all()
    order_ids = {o.id for o in orders}
    product_ids = {p.id for p in products}
    for oi in order_items:
        assert oi.order_id in order_ids, f"OrderItem {oi.id} has invalid order_id {oi.order_id}"
        assert oi.product_id in product_ids, f"OrderItem {oi.id} has invalid product_id {oi.product_id}"

    # 4. Payment -> Order
    payments = db_session.query(Payment).all()
    for pay in payments:
        assert pay.order_id in order_ids, f"Payment {pay.id} has invalid order_id {pay.order_id}"


def test_customer_uniqueness_and_validity(db_session):
    """Verify customer email and phone uniqueness in SQLite database."""
    customers = db_session.query(Customer).all()
    emails = [c.email for c in customers]
    phones = [c.phone for c in customers]

    assert len(emails) == len(set(emails)), "Customer emails must be strictly unique"
    assert len(phones) == len(set(phones)), "Customer phones must be strictly unique"
