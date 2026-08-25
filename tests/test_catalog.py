"""
WatchSphere AI v3.0 - Catalog Management Unit Tests (Phase 4)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.services.vendor_service import VendorService
from backend.services.category_service import CategoryService
from backend.services.product_service import ProductService
from backend.services.audit_log_service import AuditLogService
from backend.services.catalog_export_service import CatalogExportService


def test_vendor_crud_and_uniqueness(db_session):
    """Test Vendor creation, GST/Email duplicate checks, status toggle, and audit logging."""
    vendor_service = VendorService(db_session)
    v_data = {
        "company_name": "Krono Tech Corp",
        "owner_name": "Vikram Seth",
        "email": "krono@watchsphere.ai",
        "phone": "+91 9998887770",
        "gst_number": "27KRONO1234567Z",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India"
    }

    # Create
    ok, msg, vendor = vendor_service.create(v_data)
    assert ok is True
    assert vendor.id is not None
    assert vendor.company_name == "Krono Tech Corp"

    # Duplicate Email Check
    ok2, msg2, _ = vendor_service.create(v_data)
    assert ok2 is False
    assert "already exists" in msg2

    # Status Toggle
    ok3, msg3 = vendor_service.update_status(vendor.id, "Suspended")
    assert ok3 is True
    assert vendor.status == "Suspended"


def test_category_and_subcategory_crud(db_session):
    """Test Category and Subcategory creation and display order sorting."""
    cat_service = CategoryService(db_session)
    ok_c, _, cat = cat_service.create_category({
        "name": "Luxury Timepieces Test",
        "description": "Test Category",
        "display_order": 1
    })
    assert ok_c is True
    assert cat.id is not None

    ok_sub, _, subcat = cat_service.create_subcategory({
        "name": "Chronometer Test Sub",
        "parent_category_id": cat.id,
        "description": "Test Subcategory"
    })
    assert ok_sub is True
    assert subcat.parent_category_name == "Luxury Timepieces Test"


def test_product_crud_margin_calc_and_duplication(db_session):
    """Test Product creation, profit margin math, SKU unique check, and duplicate product action."""
    prd_service = ProductService(db_session)
    p_data = {
        "sku": "SKU-TEST-001",
        "barcode": "BAR-TEST-001",
        "name": "Test Chronograph Watch",
        "brand": "WatchSphere",
        "cost_price": 500.0,
        "selling_price": 1000.0,
        "opening_stock": 50,
        "current_stock": 50,
        "status": "Active"
    }

    # Create
    ok, msg, product = prd_service.create(p_data)
    assert ok is True
    assert product.profit_margin == 50.0  # (1000-500)/1000 * 100

    # Duplicate SKU Check
    ok2, msg2, _ = prd_service.create(p_data)
    assert ok2 is False
    assert "already exists" in msg2

    # Duplicate Product Action
    ok_dup, msg_dup, dup_product = prd_service.duplicate_product(product.id)
    assert ok_dup is True
    assert "COPY" in dup_product.sku
    assert dup_product.status == "Draft"


def test_audit_log_service(db_session):
    """Test Audit Log creation and retrieval."""
    audit_service = AuditLogService(db_session)
    log_entry = audit_service.log_event(
        entity_name="Product",
        entity_id="prod-123",
        action="Create",
        admin_email="admin@watchsphere.ai",
        previous_val=None,
        new_val={"name": "Test Product"}
    )
    assert log_entry.id is not None
    
    logs = audit_service.get_logs_for_entity("Product", "prod-123")
    assert len(logs) == 1
    assert logs[0].admin_email == "admin@watchsphere.ai"


def test_catalog_export_service():
    """Test CSV and Excel export formatting."""
    data = [{"ID": "V1", "Name": "Vendor 1"}, {"ID": "V2", "Name": "Vendor 2"}]
    csv_str = CatalogExportService.export_to_csv(data)
    assert "Vendor 1" in csv_str
    
    excel_bytes = CatalogExportService.export_to_excel_bytes(data)
    assert len(excel_bytes) > 0
