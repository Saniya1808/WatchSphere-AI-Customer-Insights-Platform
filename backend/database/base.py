"""
WatchSphere AI v3.0 - SQLAlchemy Base Importer for Alembic
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from config.database import Base
from backend.models.base_model import BaseModel
from backend.models.user import User
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.models.product import Product
from backend.models.product_image import ProductImage
from backend.models.audit_log import AuditLog
from backend.models.customer import Customer
from backend.models.customer_address import CustomerAddress
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.payment import Payment
from backend.models.inventory_transaction import InventoryTransaction
from backend.models.review import Review
from backend.models.wishlist import Wishlist
from backend.models.ml_model import MLModel
from backend.models.ml_prediction import MLPrediction
from backend.models.ml_training_log import MLTrainingLog
from backend.models.role import Role, Permission
from backend.models.notification import Notification
from backend.models.scheduled_report import ScheduledReport
from backend.models.api_key import APIKey
from backend.models.system_setting import SystemSetting
from backend.models.backup_history import BackupHistory

__all__ = [
    "Base",
    "BaseModel",
    "User",
    "Vendor",
    "Category",
    "Subcategory",
    "Product",
    "ProductImage",
    "AuditLog",
    "Customer",
    "CustomerAddress",
    "Order",
    "OrderItem",
    "Payment",
    "InventoryTransaction",
    "Review",
    "Wishlist",
    "MLModel",
    "MLPrediction",
    "MLTrainingLog",
    "Role",
    "Permission",
    "Notification",
    "ScheduledReport",
    "APIKey",
    "SystemSetting",
    "BackupHistory",
]
