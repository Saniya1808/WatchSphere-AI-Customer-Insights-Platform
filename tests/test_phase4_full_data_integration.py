"""
WatchSphere AI v3.0 - Phase 4 Comprehensive Real Data Integration Test Suite
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
from backend.services.vendor_service import VendorService
from backend.services.category_service import CategoryService
from backend.services.product_service import ProductService
from backend.services.customer_service import CustomerService
from backend.services.order_service import OrderService
from backend.services.payment_service import PaymentService
from backend.services.review_service import ReviewService
from backend.services.wishlist_service import WishlistService
from backend.services.reporting_service import ReportingService


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_csv_file_loading_and_non_empty():
    """Verify all 24 CSV datasets in datasets/ load successfully into DataFrames."""
    datasets_dir = PROJECT_ROOT / "datasets"
    all_csvs = list(datasets_dir.glob("*.csv"))
    assert len(all_csvs) >= 24

    for csv_file in all_csvs:
        df = pd.read_csv(csv_file)
        assert df is not None
        assert len(df.columns) > 0, f"CSV {csv_file.name} must have columns"


def test_service_database_access():
    """Verify all major entity services query real records from SQLite database."""
    db = SessionLocal()
    try:
        vendors = VendorService(db).get_all()
        assert len(vendors) >= 12

        categories = CategoryService(db).get_all_categories()
        assert len(categories) == 3

        products = ProductService(db).get_all()
        assert len(products) == 1000

        customers = CustomerService(db).get_all()
        assert len(customers) == 3000

        orders = OrderService(db).get_all()
        assert len(orders) == 8000

        payments = PaymentService(db).get_all()
        assert len(payments) == 8000

        reviews = ReviewService(db).get_all()
        assert len(reviews) == 5000

        wishlist = WishlistService(db).get_all()
        assert len(wishlist) == 4000
    finally:
        db.close()


def test_report_generation_from_database():
    """Verify ReportingService generates valid non-empty byte payloads for CSV, Excel, PDF."""
    db = SessionLocal()
    try:
        orders = OrderService(db).get_all()
        raw_data = [{"OrderNumber": o.order_number, "Amount": o.total_amount} for o in orders[:50]]

        csv_bytes, csv_fn = ReportingService.generate_report_bytes("Sales Report", "CSV", raw_data)
        assert len(csv_bytes) > 0
        assert csv_fn.endswith(".csv")

        excel_bytes, excel_fn = ReportingService.generate_report_bytes("Sales Report", "Excel", raw_data)
        assert len(excel_bytes) > 0
        assert excel_fn.endswith(".xlsx")

        pdf_bytes, pdf_fn = ReportingService.generate_report_bytes("Sales Report", "PDF", raw_data)
        assert len(pdf_bytes) > 0
        assert pdf_fn.endswith(".pdf")
    finally:
        db.close()
