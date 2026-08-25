"""
WatchSphere AI v3.0 - Product Entity Model
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from backend.models.base_model import BaseModel


class Product(BaseModel):
    """
    SQLAlchemy Product Model mapping catalog watch items.
    """
    __tablename__ = "products"

    sku = Column(String(100), unique=True, index=True, nullable=False)
    barcode = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    brand = Column(String(100), nullable=False)
    vendor_id = Column(String(36), ForeignKey("vendors.id"), nullable=True)
    vendor_name = Column(String(255), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    category_name = Column(String(255), nullable=False)
    subcategory_id = Column(String(36), ForeignKey("subcategories.id"), nullable=True)
    subcategory_name = Column(String(255), nullable=True)
    description = Column(String(2000), nullable=True)
    image_url = Column(String(500), nullable=True)

    # Pricing & Tax
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    gst_rate = Column(Float, default=18.0, nullable=False)
    profit_margin = Column(Float, default=0.0, nullable=False)

    # Inventory & Warehouse
    opening_stock = Column(Integer, default=0, nullable=False)
    current_stock = Column(Integer, default=0, nullable=False)
    minimum_stock = Column(Integer, default=10, nullable=False)
    warehouse = Column(String(100), default="WH-East Coast", nullable=False)
    weight = Column(Float, default=0.5, nullable=True)
    dimensions = Column(String(100), default="10x10x5 cm", nullable=True)

    # Metrics & Status
    status = Column(String(20), default="Active", nullable=False)  # Draft, Active, Hidden, Discontinued
    rating = Column(Float, default=4.8, nullable=False)

    def __repr__(self) -> str:
        return f"<Product id={self.id} sku='{self.sku}' name='{self.name}'>"
