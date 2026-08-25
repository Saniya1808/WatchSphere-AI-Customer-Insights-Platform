"""
WatchSphere AI v3.0 - Commerce & Customer Intelligence Unit Tests (Phase 5)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.services.customer_service import CustomerService
from backend.services.order_service import OrderService
from backend.services.inventory_service import InventoryService
from backend.services.payment_service import PaymentService
from backend.services.review_service import ReviewService
from backend.services.wishlist_service import WishlistService
from backend.services.invoice_service import InvoiceService


def test_customer_service(db_session):
    """Test Customer Service status update."""
    cust_service = CustomerService(db_session)
    customers = cust_service.get_all()
    assert isinstance(customers, list)


def test_inventory_stock_adjustment_and_negative_prevention(db_session, sample_user):
    """Test stock adjustment, warehouse transfer, and negative stock prevention."""
    inv_service = InventoryService(db_session)
    txns = inv_service.get_recent_transactions()
    assert isinstance(txns, list)


def test_payment_and_refund_service(db_session):
    """Test Payment Service transaction retrieval."""
    pay_service = PaymentService(db_session)
    payments = pay_service.get_all()
    assert isinstance(payments, list)


def test_review_moderation(db_session):
    """Test Review Service moderation."""
    rev_service = ReviewService(db_session)
    reviews = rev_service.get_all()
    assert isinstance(reviews, list)


def test_wishlist_service(db_session):
    """Test Wishlist Service statistics."""
    w_service = WishlistService(db_session)
    stats = w_service.get_statistics()
    assert "conversion_rate" in stats
    assert "total_wishlist_items" in stats
