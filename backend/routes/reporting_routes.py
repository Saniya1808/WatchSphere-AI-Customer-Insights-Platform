"""
WatchSphere AI v3.0 - Executive Reporting & Data Export API Routes
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, Response, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.services.reporting_service import ReportingService
from backend.services.order_service import OrderService
from backend.services.product_service import ProductService
from backend.services.customer_service import CustomerService
from backend.services.vendor_service import VendorService

router = APIRouter(prefix="/reports", tags=["Executive Reporting & Export"])


@router.get("/domains", summary="List Supported Executive Report Domains")
def list_report_domains():
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Retrieved supported report domains",
        data=ReportingService.REPORT_DOMAINS
    )


@router.get("/export", summary="Export Domain Report (CSV, Excel, PDF, HTML)")
def export_report(
    domain: str = Query("Sales Report", description="Report domain name"),
    format: str = Query("CSV", description="Export format: CSV, Excel, PDF, HTML"),
    db: Session = Depends(get_db)
):
    # Fetch real data based on requested domain
    raw_data: List[Dict[str, Any]] = []

    if "sales" in domain.lower() or "order" in domain.lower():
        orders = OrderService(db).get_all()
        raw_data = [{"OrderNumber": o.order_number, "Customer": o.customer_name, "Vendor": o.vendor_name, "Amount": o.total_amount, "Status": o.order_status, "Date": o.order_date} for o in orders[:500]]
    elif "product" in domain.lower() or "inventory" in domain.lower():
        products = ProductService(db).get_all()
        raw_data = [{"SKU": p.sku, "Name": p.name, "Brand": p.brand, "Category": p.category_name, "Price": p.selling_price, "Stock": p.current_stock} for p in products]
    elif "customer" in domain.lower():
        customers = CustomerService(db).get_all()
        raw_data = [{"Name": c.full_name, "Email": c.email, "Phone": c.phone, "City": c.city, "Segment": c.segment, "Spending": c.total_spending} for c in customers]
    elif "vendor" in domain.lower():
        vendors = VendorService(db).get_all()
        raw_data = [{"Company": v.company_name, "Owner": v.owner_name, "Email": v.email, "Phone": v.phone, "City": v.city, "Status": v.status} for v in vendors]
    else:
        raw_data = [{"Report": domain, "Status": "Active Dataset Ingested", "Generated": "2026-08-08"}]

    payload_bytes, filename = ReportingService.generate_report_bytes(domain=domain, fmt=format, data=raw_data)

    media_types = {
        "CSV": "text/csv",
        "Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "HTML": "text/html",
        "PDF": "application/pdf"
    }

    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(content=payload_bytes, media_type=media_types.get(format, "text/plain"), headers=headers)
