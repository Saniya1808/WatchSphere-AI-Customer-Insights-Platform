"""
WatchSphere AI v3.0 - Catalog Management API Routes (Vendors, Categories, Subcategories, Products)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.services.vendor_service import VendorService
from backend.services.category_service import CategoryService
from backend.services.product_service import ProductService
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.models.product import Product

router = APIRouter(tags=["Catalog Management"])


# ============================================================================
# VENDOR ENDPOINTS
# ============================================================================

@router.get("/vendors", summary="List All Vendors")
def list_vendors(
    search: Optional[str] = Query(None, description="Search term for company, owner, email, GST"),
    status_filter: Optional[str] = Query(None, alias="status", description="Status filter (Active, Suspended)"),
    db: Session = Depends(get_db)
):
    service = VendorService(db)
    vendors = service.get_all(search=search, status=status_filter)
    data = [
        {
            "id": v.id,
            "company_name": v.company_name,
            "owner_name": v.owner_name,
            "email": v.email,
            "phone": v.phone,
            "gst_number": v.gst_number,
            "city": v.city,
            "state": v.state,
            "country": v.country,
            "status": v.status,
            "rating": v.rating,
            "products_count": v.products_count,
            "revenue": v.revenue
        }
        for v in vendors
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} vendors successfully",
        data=data
    )


@router.get("/vendors/{vendor_id}", summary="Get Vendor by ID")
def get_vendor(vendor_id: str, db: Session = Depends(get_db)):
    service = VendorService(db)
    vendor = service.get_by_id(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    data = {
        "id": vendor.id,
        "company_name": vendor.company_name,
        "owner_name": vendor.owner_name,
        "email": vendor.email,
        "phone": vendor.phone,
        "gst_number": vendor.gst_number,
        "address": vendor.address,
        "city": vendor.city,
        "state": vendor.state,
        "country": vendor.country,
        "status": vendor.status,
        "rating": vendor.rating,
        "products_count": vendor.products_count,
        "revenue": vendor.revenue
    }
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Vendor retrieved successfully",
        data=data
    )


@router.post("/vendors", status_code=status.HTTP_201_CREATED, summary="Create Vendor")
def create_vendor(vendor_data: Dict[str, Any], db: Session = Depends(get_db)):
    service = VendorService(db)
    ok, msg, vendor = service.create(vendor_data)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=msg,
        data={"id": vendor.id, "company_name": vendor.company_name}
    )


# ============================================================================
# CATEGORY & SUBCATEGORY ENDPOINTS
# ============================================================================

@router.get("/categories", summary="List All Categories")
def list_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    categories = service.get_all_categories()
    data = [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "display_order": c.display_order,
            "status": c.status,
            "products_count": c.products_count
        }
        for c in categories
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} categories",
        data=data
    )


@router.get("/categories/{category_id}", summary="Get Category by ID")
def get_category(category_id: str, db: Session = Depends(get_db)):
    service = CategoryService(db)
    cat = service.get_category_by_id(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Category retrieved successfully",
        data={"id": cat.id, "name": cat.name, "description": cat.description, "status": cat.status}
    )


@router.get("/subcategories", summary="List All Subcategories")
def list_subcategories(db: Session = Depends(get_db)):
    subcats = db.query(Subcategory).order_by(Subcategory.name.asc()).all()
    data = [
        {
            "id": sc.id,
            "name": sc.name,
            "parent_category_id": sc.parent_category_id,
            "parent_category_name": sc.parent_category_name,
            "status": sc.status
        }
        for sc in subcats
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} subcategories",
        data=data
    )


# ============================================================================
# PRODUCT ENDPOINTS
# ============================================================================

@router.get("/products", summary="List All Products")
def list_products(
    search: Optional[str] = Query(None, description="Search by name, SKU, brand"),
    category: Optional[str] = Query(None, description="Category filter"),
    vendor: Optional[str] = Query(None, description="Vendor filter"),
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    products = service.get_all(search=search, category=category, vendor=vendor)
    data = [
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "brand": p.brand,
            "vendor_id": p.vendor_id,
            "vendor_name": p.vendor_name,
            "category_id": p.category_id,
            "category_name": p.category_name,
            "subcategory_name": p.subcategory_name,
            "cost_price": p.cost_price,
            "selling_price": p.selling_price,
            "discount": p.discount,
            "current_stock": p.current_stock,
            "rating": p.rating,
            "status": p.status
        }
        for p in products
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} products",
        data=data
    )


@router.get("/products/{product_id}", summary="Get Product by ID")
def get_product(product_id: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    data = {
        "id": product.id,
        "sku": product.sku,
        "barcode": product.barcode,
        "name": product.name,
        "brand": product.brand,
        "vendor_id": product.vendor_id,
        "vendor_name": product.vendor_name,
        "category_id": product.category_id,
        "category_name": product.category_name,
        "subcategory_id": product.subcategory_id,
        "subcategory_name": product.subcategory_name,
        "cost_price": product.cost_price,
        "selling_price": product.selling_price,
        "discount": product.discount,
        "current_stock": product.current_stock,
        "minimum_stock": product.minimum_stock,
        "rating": product.rating,
        "status": product.status
    }
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Product retrieved successfully",
        data=data
    )


@router.post("/products", status_code=status.HTTP_201_CREATED, summary="Create Product")
def create_product(product_data: Dict[str, Any], db: Session = Depends(get_db)):
    service = ProductService(db)
    ok, msg, product = service.create(product_data)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=msg,
        data={"id": product.id, "sku": product.sku, "name": product.name}
    )


@router.delete("/products/{product_id}", summary="Delete Product")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    ok, msg = service.delete(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail=msg)
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=msg,
        data={"deleted_id": product_id}
    )
