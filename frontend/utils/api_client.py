"""
WatchSphere AI v3.0 - Frontend API Client (FastAPI HTTP REST Integration)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any, List, Optional
import requests
from config.settings import settings
from config.database import SessionLocal
from backend.services.product_service import ProductService
from backend.services.customer_service import CustomerService
from backend.services.order_service import OrderService
from backend.services.vendor_service import VendorService
from backend.services.payment_service import PaymentService
from backend.services.review_service import ReviewService
from config.logging import logger


class APIClient:
    """
    Frontend API Client connecting Streamlit UI to FastAPI REST Endpoints (`http://127.0.0.1:8000/api/v1/...`).
    Includes fallback to in-process database services if REST backend is offline during initialization.
    """

    BASE_URL = f"http://{settings.HOST}:{settings.PORT}{settings.API_V1_PREFIX}"

    @classmethod
    def get_dashboard_kpis(cls) -> Dict[str, Any]:
        """Fetch aggregated executive KPIs from FastAPI endpoint /api/v1/dashboard/kpis."""
        try:
            res = requests.get(f"{cls.BASE_URL}/dashboard/kpis", timeout=2)
            if res.status_code == 200:
                return res.json().get("data", {})
        except Exception:
            logger.info("REST API endpoint unavailable; using in-process DB KPI calculation.")

        # In-process DB fallback
        db = SessionLocal()
        try:
            orders = OrderService(db).get_all()
            customers = CustomerService(db).get_all()
            products = ProductService(db).get_all()
            vendors = VendorService(db).get_all()
            reviews = ReviewService(db).get_all()

            tot_rev = sum(o.total_amount for o in orders) if orders else 0.0
            tot_inv = sum(p.selling_price * p.current_stock for p in products) if products else 0.0
            avg_rat = round(sum(r.rating for r in reviews) / max(1, len(reviews)), 2) if reviews else 4.75

            return {
                "total_revenue": {"title": "Total Revenue", "value": f"${tot_rev:,.2f}", "numeric_value": float(tot_rev)},
                "total_orders": {"title": "Total Orders", "value": f"{len(orders):,}", "numeric_value": len(orders)},
                "total_customers": {"title": "Total Customers", "value": f"{len(customers):,}", "numeric_value": len(customers)},
                "total_products": {"title": "Total Products", "value": f"{len(products):,}", "numeric_value": len(products)},
                "total_vendors": {"title": "Total Vendors", "value": f"{len(vendors):,}", "numeric_value": len(vendors)},
                "inventory_value": {"title": "Inventory Value", "value": f"${tot_inv:,.2f}", "numeric_value": float(tot_inv)},
                "average_rating": {"title": "Average Rating", "value": f"⭐ {avg_rat}", "numeric_value": avg_rat}
            }
        finally:
            db.close()

    @classmethod
    def get_products(cls, search: Optional[str] = None, category: Optional[str] = None, vendor: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch catalog products from FastAPI endpoint /api/v1/products."""
        try:
            params = {}
            if search: params["search"] = search
            if category: params["category"] = category
            if vendor: params["vendor"] = vendor
            res = requests.get(f"{cls.BASE_URL}/products", params=params, timeout=2)
            if res.status_code == 200:
                return res.json().get("data", [])
        except Exception:
            pass

        db = SessionLocal()
        try:
            prods = ProductService(db).get_all(search=search, category=category, vendor=vendor)
            return [
                {"id": p.id, "sku": p.sku, "name": p.name, "brand": p.brand, "category_name": p.category_name, "vendor_name": p.vendor_name, "selling_price": p.selling_price, "current_stock": p.current_stock, "status": p.status}
                for p in prods
            ]
        finally:
            db.close()
