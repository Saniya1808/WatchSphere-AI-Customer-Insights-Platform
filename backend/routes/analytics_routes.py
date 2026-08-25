"""
WatchSphere AI v3.0 - Analytics API Routes (Sales, Geography, RFM, ABC-XYZ, Performance)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.product import Product
from backend.models.customer import Customer
from backend.models.vendor import Vendor
from backend.services.commerce_bi_analytics_service import CommerceBIAnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics & BI Engine"])


@router.get("/sales-summary", summary="Get Sales Overview Breakdown")
def get_sales_summary(db: Session = Depends(get_db)):
    """
    Returns total sales, order volume, and revenue aggregations calculated from real database orders.
    """
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0.0
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    total_items_sold = db.query(func.sum(OrderItem.quantity)).scalar() or 0
    avg_order_val = db.query(func.avg(Order.total_amount)).scalar() or 0.0

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Sales summary retrieved successfully",
        data={
            "total_revenue": round(float(total_revenue), 2),
            "total_orders": int(total_orders),
            "total_units_sold": int(total_items_sold),
            "avg_order_value": round(float(avg_order_val), 2)
        }
    )


@router.get("/category-sales", summary="Get Revenue Breakdown by Category")
def get_category_sales(db: Session = Depends(get_db)):
    """
    Aggregates product sales revenue grouped by Category from database records.
    """
    results = (
        db.query(
            Product.category_name,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            func.sum(OrderItem.quantity).label("units_sold")
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .group_by(Product.category_name)
        .all()
    )

    data = [
        {
            "category": r[0] or "Uncategorized",
            "revenue": round(float(r[1] or 0.0), 2),
            "units_sold": int(r[2] or 0)
        }
        for r in results
    ]

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved sales data across {len(data)} categories",
        data=data
    )


@router.get("/vendor-sales", summary="Get Revenue Breakdown by Vendor")
def get_vendor_sales(db: Session = Depends(get_db)):
    """
    Aggregates product sales revenue grouped by Vendor from database records.
    """
    results = (
        db.query(
            Product.vendor_name,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            func.sum(OrderItem.quantity).label("units_sold")
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .group_by(Product.vendor_name)
        .all()
    )

    data = [
        {
            "vendor": r[0] or "Unknown Vendor",
            "revenue": round(float(r[1] or 0.0), 2),
            "units_sold": int(r[2] or 0)
        }
        for r in results
    ]

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved sales data across {len(data)} vendors",
        data=data
    )


@router.get("/bi/rfm", summary="Get RFM Customer Segmentation Matrix")
def get_rfm_analytics(db: Session = Depends(get_db)):
    """
    Calculates Recency, Frequency, Monetary (RFM) customer segmentation from database order history.
    """
    rfm_df = CommerceBIAnalyticsService.calculate_rfm_segmentation(db)
    records = rfm_df.head(50).to_dict(orient="records") if not rfm_df.empty else []
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Calculated RFM metrics for {len(records)} customer records",
        data=records
    )


@router.get("/bi/abc-xyz", summary="Get ABC-XYZ Inventory Classification")
def get_abc_xyz_analytics(db: Session = Depends(get_db)):
    """
    Calculates ABC-XYZ Inventory matrix classification based on product revenue contribution and demand volatility.
    """
    abc_df = CommerceBIAnalyticsService.calculate_abc_xyz_analysis(db)
    records = abc_df.head(50).to_dict(orient="records") if not abc_df.empty else []
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Calculated ABC-XYZ matrix for {len(records)} catalog products",
        data=records
    )
