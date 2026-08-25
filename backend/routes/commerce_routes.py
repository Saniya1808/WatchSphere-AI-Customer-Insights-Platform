"""
WatchSphere AI v3.0 - Commerce API Routes (Customers, Orders, OrderItems, Payments, Inventory, Reviews, Wishlist)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.services.customer_service import CustomerService
from backend.services.order_service import OrderService
from backend.services.payment_service import PaymentService
from backend.services.inventory_service import InventoryService
from backend.services.review_service import ReviewService
from backend.services.wishlist_service import WishlistService
from backend.models.order_item import OrderItem
from backend.models.product_image import ProductImage

router = APIRouter(tags=["Commerce Operations"])


# ============================================================================
# CUSTOMERS ENDPOINTS
# ============================================================================

@router.get("/customers", summary="List All Customers")
def list_customers(
    search: Optional[str] = Query(None, description="Search term for name, email, phone, city"),
    segment: Optional[str] = Query(None, description="Segment filter"),
    db: Session = Depends(get_db)
):
    service = CustomerService(db)
    customers = service.get_all(search=search, segment=segment)
    data = [
        {
            "id": c.id,
            "full_name": c.full_name,
            "email": c.email,
            "phone": c.phone,
            "gender": c.gender,
            "age": c.age,
            "city": c.city,
            "state": c.state,
            "segment": c.segment,
            "status": c.status,
            "total_spending": c.total_spending,
            "orders_count": c.orders_count
        }
        for c in customers
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} customers",
        data=data
    )


@router.get("/customers/{customer_id}", summary="Get Customer by ID")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    service = CustomerService(db)
    customer = service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    data = {
        "id": customer.id,
        "full_name": customer.full_name,
        "email": customer.email,
        "phone": customer.phone,
        "gender": customer.gender,
        "age": customer.age,
        "city": customer.city,
        "state": customer.state,
        "country": customer.country,
        "segment": customer.segment,
        "status": customer.status,
        "orders_count": customer.orders_count,
        "total_spending": customer.total_spending,
        "avg_order_value": customer.avg_order_value,
        "last_purchase_date": customer.last_purchase_date
    }
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Customer profile retrieved successfully",
        data=data
    )


# ============================================================================
# ORDERS & ORDER ITEMS ENDPOINTS
# ============================================================================

@router.get("/orders", summary="List All Orders")
def list_orders(
    search: Optional[str] = Query(None, description="Search by order number or customer name"),
    order_status: Optional[str] = Query(None, alias="status", description="Order status filter"),
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    orders = service.get_all(search=search, order_status=order_status)
    data = [
        {
            "id": o.id,
            "order_number": o.order_number,
            "customer_id": o.customer_id,
            "customer_name": o.customer_name,
            "vendor_name": o.vendor_name,
            "total_amount": o.total_amount,
            "final_amount": o.final_amount,
            "payment_method": o.payment_method,
            "payment_status": o.payment_status,
            "order_status": o.order_status,
            "order_date": o.order_date
        }
        for o in orders
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} orders",
        data=data
    )


@router.get("/orders/{order_id}", summary="Get Order Details")
def get_order(order_id: str, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    data = {
        "id": order.id,
        "order_number": order.order_number,
        "customer_id": order.customer_id,
        "customer_name": order.customer_name,
        "vendor_id": order.vendor_id,
        "vendor_name": order.vendor_name,
        "total_amount": order.total_amount,
        "discount_amount": order.discount_amount,
        "gst_amount": order.gst_amount,
        "final_amount": order.final_amount,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "order_status": order.order_status,
        "order_date": order.order_date,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "sku": item.sku,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal
            }
            for item in items
        ]
    }
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Order details retrieved successfully",
        data=data
    )


@router.get("/order-items", summary="List Order Items")
def list_order_items(db: Session = Depends(get_db)):
    items = db.query(OrderItem).all()
    data = [
        {
            "id": oi.id,
            "order_id": oi.order_id,
            "product_id": oi.product_id,
            "product_name": oi.product_name,
            "sku": oi.sku,
            "quantity": oi.quantity,
            "unit_price": oi.unit_price,
            "subtotal": oi.subtotal
        }
        for oi in items
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} order items",
        data=data
    )


# ============================================================================
# PAYMENTS ENDPOINTS
# ============================================================================

@router.get("/payments", summary="List All Payments")
def list_payments(db: Session = Depends(get_db)):
    service = PaymentService(db)
    payments = service.get_all()
    data = [
        {
            "id": p.id,
            "order_id": p.order_id,
            "order_number": p.order_number,
            "customer_id": p.customer_id,
            "customer_name": p.customer_name,
            "payment_method": p.payment_method,
            "transaction_id": p.transaction_id,
            "amount": p.amount,
            "status": p.status,
            "payment_date": p.payment_date
        }
        for p in payments
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} payment transactions",
        data=data
    )


# ============================================================================
# INVENTORY ENDPOINTS
# ============================================================================

@router.get("/inventory", summary="Get Inventory Levels")
def get_inventory(db: Session = Depends(get_db)):
    from backend.models.product import Product
    products = db.query(Product).all()
    inventory = [
        {
            "id": p.id,
            "sku": p.sku,
            "product_name": p.name,
            "warehouse": p.warehouse,
            "current_stock": p.current_stock,
            "minimum_stock": p.minimum_stock,
            "status": p.status
        }
        for p in products
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(inventory)} inventory product records",
        data=inventory
    )


# ============================================================================
# REVIEWS & WISHLIST ENDPOINTS
# ============================================================================

@router.get("/reviews", summary="List All Reviews")
def list_reviews(db: Session = Depends(get_db)):
    service = ReviewService(db)
    reviews = service.get_all()
    data = [
        {
            "id": r.id,
            "customer_id": r.customer_id,
            "customer_name": r.customer_name,
            "product_id": r.product_id,
            "product_name": r.product_name,
            "rating": r.rating,
            "title": r.title,
            "review_text": r.review_text,
            "sentiment": r.sentiment,
            "status": r.status
        }
        for r in reviews
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} customer reviews",
        data=data
    )


@router.get("/wishlist", summary="List Wishlist Items")
def list_wishlist(db: Session = Depends(get_db)):
    service = WishlistService(db)
    items = service.get_all()
    data = [
        {
            "id": w.id,
            "customer_id": w.customer_id,
            "customer_name": w.customer_name,
            "product_id": w.product_id,
            "product_name": w.product_name,
            "category": w.category,
            "brand": w.brand,
            "status": w.status
        }
        for w in items
    ]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} wishlist items",
        data=data
    )


@router.get("/product-images", summary="List Product Images")
def list_product_images(db: Session = Depends(get_db)):
    images = db.query(ProductImage).all()
    data = [{"id": img.id, "product_id": img.product_id, "image_url": img.image_url} for img in images]
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(data)} product images",
        data=data
    )
