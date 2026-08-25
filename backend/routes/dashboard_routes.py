"""
WatchSphere AI v3.0 - Executive Dashboard API Routes (Real-Time Database Aggregation)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.models.vendor import Vendor
from backend.models.product import Product
from backend.models.customer import Customer
from backend.models.order import Order
from backend.models.payment import Payment
from backend.models.review import Review
from backend.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Executive Dashboard"])


@router.get("/kpis", summary="Get Aggregated Executive KPIs")
def get_dashboard_kpis(db: Session = Depends(get_db)):
    """
    Computes executive business metrics via direct SQL/SQLAlchemy database aggregation.
    No fake or hardcoded fallbacks used.
    """
    tot_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0.0
    tot_orders = db.query(func.count(Order.id)).scalar() or 0
    tot_customers = db.query(func.count(Customer.id)).scalar() or 0
    tot_products = db.query(func.count(Product.id)).scalar() or 0
    tot_vendors = db.query(func.count(Vendor.id)).scalar() or 0
    
    inv_value = db.query(func.sum(Product.current_stock * Product.selling_price)).scalar() or 0.0
    avg_rating_rev = db.query(func.avg(Review.rating)).scalar()
    avg_rating_prod = db.query(func.avg(Product.rating)).scalar()
    avg_rating = float(avg_rating_rev if avg_rating_rev is not None else (avg_rating_prod or 0.0))
    
    avg_order_val = db.query(func.avg(Order.total_amount)).scalar() or 0.0
    pending_payments = db.query(func.sum(Payment.amount)).filter(Payment.status == "Pending").scalar() or 0.0
    low_stock = db.query(func.count(Product.id)).filter(Product.current_stock < Product.minimum_stock).scalar() or 0

    kpis = {
        "total_revenue": {
            "title": "Total Revenue",
            "value": f"${tot_revenue:,.2f}",
            "numeric_value": float(tot_revenue)
        },
        "total_orders": {
            "title": "Total Orders",
            "value": f"{tot_orders:,}",
            "numeric_value": int(tot_orders)
        },
        "total_customers": {
            "title": "Total Customers",
            "value": f"{tot_customers:,}",
            "numeric_value": int(tot_customers)
        },
        "total_products": {
            "title": "Total Products",
            "value": f"{tot_products:,}",
            "numeric_value": int(tot_products)
        },
        "total_vendors": {
            "title": "Total Vendors",
            "value": f"{tot_vendors:,}",
            "numeric_value": int(tot_vendors)
        },
        "inventory_value": {
            "title": "Inventory Value",
            "value": f"${inv_value:,.2f}",
            "numeric_value": float(inv_value)
        },
        "average_rating": {
            "title": "Average Rating",
            "value": f"⭐ {avg_rating:.2f} / 5.0",
            "numeric_value": round(avg_rating, 2)
        },
        "average_order_value": {
            "title": "Average Order Value",
            "value": f"${avg_order_val:,.2f}",
            "numeric_value": float(avg_order_val)
        },
        "pending_payments": {
            "title": "Pending Payments",
            "value": f"${pending_payments:,.2f}",
            "numeric_value": float(pending_payments)
        },
        "low_stock_products": {
            "title": "Low Stock Products",
            "value": f"{low_stock:,}",
            "numeric_value": int(low_stock)
        }
    }

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Dashboard executive KPIs calculated successfully from database",
        data=kpis
    )


@router.get("/summary", summary="Get Executive Dashboard Intelligence & Alerts")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Retrieves real-time alerts, cross-module intelligence cards, and AI executive summary.
    """
    alerts = DashboardService.get_realtime_alerts()
    intelligence = DashboardService.get_cross_module_intelligence()
    ai_summary = DashboardService.get_ai_executive_summary()

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Dashboard executive summary retrieved successfully",
        data={
            "alerts": alerts,
            "intelligence": intelligence,
            "ai_summary": ai_summary
        }
    )
