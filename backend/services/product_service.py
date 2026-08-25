"""
WatchSphere AI v3.0 - Product CRUD Repository Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import uuid
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.services.audit_log_service import AuditLogService
from config.logging import logger


class ProductService:
    """
    CRUD Repository service for Product entities with SKU/Barcode unique validation, profit margin math, and audit logs.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Fetch product by ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Fetch product by SKU."""
        return self.db.query(Product).filter(Product.sku == sku.upper().strip()).first()

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        """Fetch product by Barcode."""
        return self.db.query(Product).filter(Product.barcode == barcode.strip()).first()

    def get_all(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        vendor: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Product]:
        """Retrieve products with optional filtering."""
        query = self.db.query(Product)
        if status and status != "All Statuses":
            query = query.filter(Product.status == status)
        if category and category != "All Categories":
            query = query.filter(Product.category_name == category)
        if vendor and vendor != "All Vendors":
            query = query.filter(Product.vendor_name == vendor)
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                (Product.name.ilike(search_term)) |
                (Product.sku.ilike(search_term)) |
                (Product.brand.ilike(search_term)) |
                (Product.barcode.ilike(search_term))
            )
        return query.order_by(Product.created_at.desc()).all()

    def create(self, p_data: Dict[str, Any], admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, Optional[Product]]:
        """
        Creates a new product record after validating unique SKU and Barcode.
        Calculates profit margin automatically.
        """
        sku = p_data.get("sku", "").upper().strip()
        barcode = p_data.get("barcode", "").strip()

        if self.get_by_sku(sku):
            return False, f"Product SKU '{sku}' already exists.", None

        if self.get_by_barcode(barcode):
            return False, f"Product Barcode '{barcode}' already exists.", None

        cost_price = float(p_data.get("cost_price", 0.0))
        selling_price = float(p_data.get("selling_price", 0.0))
        margin = ((selling_price - cost_price) / selling_price * 100) if selling_price > 0 else 0.0

        try:
            product = Product(
                sku=sku,
                barcode=barcode,
                name=p_data.get("name"),
                brand=p_data.get("brand", "WatchSphere"),
                vendor_id=p_data.get("vendor_id"),
                vendor_name=p_data.get("vendor_name", "Acme Watch Co."),
                category_id=p_data.get("category_id"),
                category_name=p_data.get("category_name", "Smartwatches"),
                subcategory_id=p_data.get("subcategory_id"),
                subcategory_name=p_data.get("subcategory_name"),
                description=p_data.get("description"),
                image_url=p_data.get("image_url"),
                cost_price=cost_price,
                selling_price=selling_price,
                discount=float(p_data.get("discount", 0.0)),
                gst_rate=float(p_data.get("gst_rate", 18.0)),
                profit_margin=round(margin, 2),
                opening_stock=int(p_data.get("opening_stock", 0)),
                current_stock=int(p_data.get("current_stock", p_data.get("opening_stock", 0))),
                minimum_stock=int(p_data.get("minimum_stock", 10)),
                warehouse=p_data.get("warehouse", "WH-East Coast"),
                weight=float(p_data.get("weight", 0.5)),
                dimensions=p_data.get("dimensions", "10x10x5 cm"),
                status=p_data.get("status", "Active"),
                rating=float(p_data.get("rating", 4.8))
            )
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)

            self.audit_service.log_event("Product", product.id, "Create", admin_email, None, p_data)
            return True, f"Product '{product.name}' registered successfully.", product
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating product: {str(e)}")
            return False, f"Product creation failed: {str(e)}", None

    def duplicate_product(self, product_id: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, Optional[Product]]:
        """Clones an existing product into a new draft product with unique SKU/Barcode."""
        original = self.get_by_id(product_id)
        if not original:
            return False, "Original product not found.", None

        new_sku = f"{original.sku}-COPY-{uuid.uuid4().hex[:4].upper()}"
        new_barcode = f"BAR-{uuid.uuid4().hex[:8].upper()}"

        p_data = {
            "sku": new_sku,
            "barcode": new_barcode,
            "name": f"{original.name} (Copy)",
            "brand": original.brand,
            "vendor_id": original.vendor_id,
            "vendor_name": original.vendor_name,
            "category_id": original.category_id,
            "category_name": original.category_name,
            "subcategory_id": original.subcategory_id,
            "subcategory_name": original.subcategory_name,
            "description": original.description,
            "image_url": original.image_url,
            "cost_price": original.cost_price,
            "selling_price": original.selling_price,
            "discount": original.discount,
            "gst_rate": original.gst_rate,
            "opening_stock": original.current_stock,
            "current_stock": original.current_stock,
            "minimum_stock": original.minimum_stock,
            "warehouse": original.warehouse,
            "weight": original.weight,
            "dimensions": original.dimensions,
            "status": "Draft",
            "rating": original.rating
        }
        return self.create(p_data, admin_email)

    def bulk_action(self, product_ids: List[str], action: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[int, str]:
        """Bulk action handler (Delete, Activate, Disable)."""
        count = 0
        for p_id in product_ids:
            product = self.get_by_id(p_id)
            if product:
                if action == "Delete":
                    self.db.delete(product)
                    self.audit_service.log_event("Product", p_id, "Delete", admin_email, {"sku": product.sku}, None)
                    count += 1
                elif action in ["Activate", "Disable"]:
                    prev = product.status
                    product.status = "Active" if action == "Activate" else "Hidden"
                    self.audit_service.log_event("Product", p_id, f"SetStatus_{product.status}", admin_email, {"status": prev}, {"status": product.status})
                    count += 1

        self.db.commit()
        return count, f"Successfully performed '{action}' on {count} products."
