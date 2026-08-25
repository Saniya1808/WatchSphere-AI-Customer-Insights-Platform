"""
WatchSphere AI v3.0 - Category & Subcategory Repository Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.services.audit_log_service import AuditLogService
from config.logging import logger


class CategoryService:
    """
    CRUD Repository service for Category and Subcategory entities.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    # ================= CATEGORY METHODS =================
    def get_all_categories(self, search: Optional[str] = None) -> List[Category]:
        """Fetch all categories ordered by display_order."""
        query = self.db.query(Category)
        if search:
            query = query.filter(Category.name.ilike(f"%{search.strip()}%"))
        return query.order_by(Category.display_order.asc(), Category.name.asc()).all()

    def create_category(self, cat_data: Dict[str, Any], admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, Optional[Category]]:
        """Create new category."""
        name = cat_data.get("name", "").strip()
        existing = self.db.query(Category).filter(Category.name == name).first()
        if existing:
            return False, f"Category '{name}' already exists.", None

        try:
            category = Category(
                name=name,
                image_url=cat_data.get("image_url"),
                description=cat_data.get("description"),
                display_order=cat_data.get("display_order", 1),
                status=cat_data.get("status", "Active")
            )
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)

            self.audit_service.log_event("Category", category.id, "Create", admin_email, None, cat_data)
            return True, f"Category '{name}' created successfully.", category
        except Exception as e:
            self.db.rollback()
            return False, f"Creation failed: {str(e)}", None

    def toggle_category_status(self, category_id: str, new_status: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Toggles category status ('Active' or 'Hidden')."""
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return False, "Category not found."

        prev = category.status
        category.status = new_status
        self.db.commit()
        self.audit_service.log_event("Category", category.id, f"SetStatus_{new_status}", admin_email, {"status": prev}, {"status": new_status})
        return True, f"Category status set to '{new_status}'."

    # ================= SUBCATEGORY METHODS =================
    def get_all_subcategories(self, parent_id: Optional[str] = None) -> List[Subcategory]:
        """Fetch all subcategories."""
        query = self.db.query(Subcategory)
        if parent_id:
            query = query.filter(Subcategory.parent_category_id == parent_id)
        return query.order_by(Subcategory.name.asc()).all()

    def create_subcategory(self, sub_data: Dict[str, Any], admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, Optional[Subcategory]]:
        """Create new subcategory."""
        name = sub_data.get("name", "").strip()
        parent_id = sub_data.get("parent_category_id")
        
        parent_cat = self.db.query(Category).filter(Category.id == parent_id).first()
        if not parent_cat:
            return False, "Parent Category not found.", None

        try:
            subcategory = Subcategory(
                name=name,
                parent_category_id=parent_cat.id,
                parent_category_name=parent_cat.name,
                image_url=sub_data.get("image_url"),
                description=sub_data.get("description"),
                status=sub_data.get("status", "Active")
            )
            self.db.add(subcategory)
            self.db.commit()
            self.db.refresh(subcategory)

            self.audit_service.log_event("Subcategory", subcategory.id, "Create", admin_email, None, sub_data)
            return True, f"Subcategory '{name}' created successfully under '{parent_cat.name}'.", subcategory
        except Exception as e:
            self.db.rollback()
            return False, f"Creation failed: {str(e)}", None
