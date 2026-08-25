"""
WatchSphere AI v3.0 - Inventory Management & Stock Adjustment Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.models.inventory_transaction import InventoryTransaction
from backend.services.audit_log_service import AuditLogService
from config.logging import logger


class InventoryService:
    """
    Inventory service supporting Stock In, Stock Out, Adjust Stock, and Warehouse Transfer with negative stock guards.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def adjust_stock(
        self,
        product_id: str,
        transaction_type: str,  # Stock In, Stock Out, Adjust Stock, Warehouse Transfer
        quantity: int,
        warehouse: str,
        notes: str = "",
        performed_by: str = "admin@watchsphere.ai"
    ) -> Tuple[bool, str]:
        """
        Executes stock modification while preventing negative inventory levels.
        """
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False, "Product not found."

        prev_stock = product.current_stock

        if transaction_type in ["Stock Out", "Warehouse Transfer"]:
            if prev_stock < quantity:
                return False, f"Insufficient stock! Available: {prev_stock}, Requested: {quantity}."
            new_stock = prev_stock - quantity
        elif transaction_type == "Stock In":
            new_stock = prev_stock + quantity
        else:  # Adjust Stock
            new_stock = max(0, quantity)

        product.current_stock = new_stock
        if transaction_type == "Warehouse Transfer":
            product.warehouse = warehouse

        txn = InventoryTransaction(
            product_id=product.id,
            product_name=product.name,
            sku=product.sku,
            warehouse=warehouse,
            transaction_type=transaction_type,
            quantity=quantity,
            previous_stock=prev_stock,
            new_stock=new_stock,
            notes=notes,
            performed_by=performed_by
        )
        self.db.add(txn)
        self.db.commit()

        self.audit_service.log_event("Inventory", product.id, f"Stock_{transaction_type}", performed_by, {"stock": prev_stock}, {"stock": new_stock})
        return True, f"Successfully executed '{transaction_type}' ({quantity} units). New Stock: {new_stock}."

    def get_recent_transactions(self, limit: int = 50) -> List[InventoryTransaction]:
        """Fetch recent stock transaction logs."""
        return self.db.query(InventoryTransaction).order_by(InventoryTransaction.created_at.desc()).limit(limit).all()
