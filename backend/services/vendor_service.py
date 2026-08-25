"""
WatchSphere AI v3.0 - Vendor CRUD Service Repository
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from backend.models.vendor import Vendor
from backend.services.audit_log_service import AuditLogService
from backend.core.exceptions import DuplicateResourceException, ResourceNotFoundException
from config.logging import logger


class VendorService:
    """
    CRUD Repository pattern service for Vendor entities with Email/GST unique checks and audit logging.
    """

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditLogService(db)

    def get_by_id(self, vendor_id: str) -> Optional[Vendor]:
        """Fetch vendor by ID."""
        return self.db.query(Vendor).filter(Vendor.id == vendor_id).first()

    def get_by_email(self, email: str) -> Optional[Vendor]:
        """Fetch vendor by email."""
        return self.db.query(Vendor).filter(Vendor.email == email.lower().strip()).first()

    def get_by_gst(self, gst_number: str) -> Optional[Vendor]:
        """Fetch vendor by GST number."""
        return self.db.query(Vendor).filter(Vendor.gst_number == gst_number.upper().strip()).first()

    def get_all(self, search: Optional[str] = None, status: Optional[str] = None) -> List[Vendor]:
        """Retrieve vendors with optional search and status filter."""
        query = self.db.query(Vendor)
        if status and status != "All Statuses":
            query = query.filter(Vendor.status == status)
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                (Vendor.company_name.ilike(search_term)) |
                (Vendor.owner_name.ilike(search_term)) |
                (Vendor.email.ilike(search_term)) |
                (Vendor.gst_number.ilike(search_term))
            )
        return query.order_by(Vendor.created_at.desc()).all()

    def create(self, vendor_data: Dict[str, Any], admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str, Optional[Vendor]]:
        """
        Creates a new Vendor record after verifying unique Email and GST constraints.
        """
        email = vendor_data.get("email", "").lower().strip()
        gst = vendor_data.get("gst_number", "").upper().strip()

        if self.get_by_email(email):
            return False, f"Vendor with email '{email}' already exists.", None

        if self.get_by_gst(gst):
            return False, f"Vendor with GST Number '{gst}' already exists.", None

        try:
            vendor = Vendor(
                company_name=vendor_data.get("company_name"),
                logo_url=vendor_data.get("logo_url"),
                owner_name=vendor_data.get("owner_name"),
                email=email,
                phone=vendor_data.get("phone", ""),
                gst_number=gst,
                address=vendor_data.get("address"),
                city=vendor_data.get("city", "Mumbai"),
                state=vendor_data.get("state", "Maharashtra"),
                country=vendor_data.get("country", "India"),
                status=vendor_data.get("status", "Active"),
                products_count=vendor_data.get("products_count", 0),
                revenue=vendor_data.get("revenue", 0.0),
                rating=vendor_data.get("rating", 4.8)
            )
            self.db.add(vendor)
            self.db.commit()
            self.db.refresh(vendor)

            # Audit Log
            self.audit_service.log_event("Vendor", vendor.id, "Create", admin_email, None, vendor_data)
            return True, "Vendor registered successfully.", vendor
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating vendor: {str(e)}")
            return False, f"Creation failed: {str(e)}", None

    def update_status(self, vendor_id: str, new_status: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[bool, str]:
        """Toggles vendor status ('Active' or 'Suspended')."""
        vendor = self.get_by_id(vendor_id)
        if not vendor:
            return False, "Vendor not found."

        prev_status = vendor.status
        vendor.status = new_status
        self.db.commit()

        self.audit_service.log_event("Vendor", vendor.id, f"SetStatus_{new_status}", admin_email, {"status": prev_status}, {"status": new_status})
        return True, f"Vendor status updated to '{new_status}'."

    def bulk_action(self, vendor_ids: List[str], action: str, admin_email: str = "admin@watchsphere.ai") -> Tuple[int, str]:
        """Performs bulk action (Delete, Activate, Suspend) across vendor IDs."""
        count = 0
        for v_id in vendor_ids:
            if action == "Delete":
                vendor = self.get_by_id(v_id)
                if vendor:
                    self.db.delete(vendor)
                    self.audit_service.log_event("Vendor", v_id, "Delete", admin_email, {"company": vendor.company_name}, None)
                    count += 1
            elif action in ["Activate", "Suspend"]:
                target_status = "Active" if action == "Activate" else "Suspended"
                ok, _ = self.update_status(v_id, target_status, admin_email)
                if ok:
                    count += 1

        self.db.commit()
        return count, f"Successfully performed '{action}' on {count} vendors."
