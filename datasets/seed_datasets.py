"""
WatchSphere AI v3.0 - Master Enterprise Datasets Scanner & Auto Seeder
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import sys
import time
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.database import SessionLocal, Base, engine
import backend.database.base
from backend.models.user import User
from backend.models.vendor import Vendor
from backend.models.category import Category
from backend.models.subcategory import Subcategory
from backend.models.product import Product
from backend.models.customer import Customer
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.payment import Payment
from backend.models.review import Review
from backend.models.wishlist import Wishlist
from backend.models.product_image import ProductImage
from config.security import hash_password
from config.logging import logger


def auto_seed_datasets():
    """
    Scans datasets/ folder for WatchSphere CSV files, validates, cleans,
    and automatically ingests master dataset records into SQLite if tables are empty.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    start_time = time.time()
    try:
        # Check if already seeded with complete dataset
        v_count = db.query(Vendor).count()
        p_count = db.query(Product).count()
        o_count = db.query(Order).count()
        c_count = db.query(Customer).count()
        if v_count >= 12 and p_count >= 1000 and o_count >= 8000 and c_count >= 3000:
            logger.info("Database contains complete master dataset records. Auto-import skipped.")
            return

        logger.info("First application startup or incomplete dataset detected. Ingesting WatchSphere master datasets into SQLite...")

        dataset_dir = project_root / "datasets"
        if not dataset_dir.exists():
            dataset_dir = project_root / "dataset"

        # 1. Seed Default Admin & Vendor accounts
        admin = db.query(User).filter(User.email == "admin@watchsphere.ai").first()
        if not admin:
            db.add(User(
                email="admin@watchsphere.ai",
                hashed_password=hash_password("Admin@123"),
                full_name="Enterprise Admin",
                role="ADMIN",
                is_active=True
            ))

        vendor_u = db.query(User).filter(User.email == "vendor@watchsphere.ai").first()
        if not vendor_u:
            db.add(User(
                email="vendor@watchsphere.ai",
                hashed_password=hash_password("Vendor@123"),
                full_name="Acme Watch Partner",
                vendor_company="Acme Watch Co.",
                role="VENDOR",
                is_active=True
            ))
        db.commit()

        # 2. Ingest Vendors
        vendors_csv = dataset_dir / "vendors.csv"
        vendor_id_lookup = {}
        if vendors_csv.exists():
            df_v = pd.read_csv(vendors_csv)
            if db.query(Vendor).count() < len(df_v):
                db.query(Vendor).delete()
                vendor_maps = []
                for _, row in df_v.iterrows():
                    v_id_num = int(row["VendorID"])
                    v_id_str = f"vend-{v_id_num}"
                    v_name = str(row["CompanyName"])
                    vendor_id_lookup[v_id_num] = (v_id_str, v_name)
                    vendor_maps.append({
                        "id": v_id_str,
                        "company_name": v_name,
                        "owner_name": str(row["OwnerName"]),
                        "email": str(row["Email"]),
                        "phone": str(row["Phone"]),
                        "gst_number": str(row["GSTNumber"]),
                        "address": str(row["Address"]),
                        "city": str(row["City"]),
                        "state": str(row["State"]) if pd.notnull(row["State"]) else "State HQ",
                        "country": "India",
                        "status": str(row.get("Status", "Active")),
                        "rating": 4.8,
                        "revenue": 0.0,
                        "is_active": True
                    })
                db.bulk_insert_mappings(Vendor, vendor_maps)
                db.commit()
                logger.info(f"Successfully imported {len(vendor_maps)} Vendors into SQLite.")
        
        # Populate lookup if existing
        if not vendor_id_lookup:
            for v in db.query(Vendor).all():
                try:
                    num_id = int(v.id.replace("vend-", ""))
                    vendor_id_lookup[num_id] = (v.id, v.company_name)
                except Exception:
                    pass

        # 3. Ingest Categories
        cats_csv = dataset_dir / "categories.csv"
        cat_id_lookup = {}
        if cats_csv.exists():
            df_c = pd.read_csv(cats_csv)
            if db.query(Category).count() < len(df_c):
                db.query(Category).delete()
                cat_maps = []
                for _, row in df_c.iterrows():
                    c_id_num = int(row["CategoryID"])
                    c_id_str = f"cat-{c_id_num}"
                    c_name = str(row["CategoryName"])
                    cat_id_lookup[c_id_num] = (c_id_str, c_name)
                    cat_maps.append({
                        "id": c_id_str,
                        "name": c_name,
                        "description": f"{c_name} Catalog Division",
                        "display_order": c_id_num,
                        "status": "Active",
                        "is_active": True
                    })
                db.bulk_insert_mappings(Category, cat_maps)
                db.commit()
                logger.info(f"Successfully imported {len(cat_maps)} Categories into SQLite.")

        if not cat_id_lookup:
            for c in db.query(Category).all():
                try:
                    num_id = int(c.id.replace("cat-", ""))
                    cat_id_lookup[num_id] = (c.id, c.name)
                except Exception:
                    pass

        # 4. Ingest Subcategories
        sc_csv = dataset_dir / "subcategories.csv"
        sc_id_lookup = {}
        if sc_csv.exists():
            df_sc = pd.read_csv(sc_csv)
            if db.query(Subcategory).count() < len(df_sc):
                db.query(Subcategory).delete()
                sc_maps = []
                for _, row in df_sc.iterrows():
                    sc_id_num = int(row["SubCategoryID"])
                    sc_id_str = f"subcat-{sc_id_num}"
                    c_id_num = int(row["CategoryID"])
                    sc_name = str(row["SubCategoryName"])
                    c_info = cat_id_lookup.get(c_id_num, (f"cat-{c_id_num}", "Category"))
                    sc_id_lookup[sc_id_num] = (sc_id_str, sc_name)
                    sc_maps.append({
                        "id": sc_id_str,
                        "name": sc_name,
                        "parent_category_id": c_info[0],
                        "parent_category_name": c_info[1],
                        "description": f"{sc_name} Watch Subcategory",
                        "status": "Active",
                        "is_active": True
                    })
                db.bulk_insert_mappings(Subcategory, sc_maps)
                db.commit()
                logger.info(f"Successfully imported {len(sc_maps)} Subcategories into SQLite.")

        if not sc_id_lookup:
            for sc in db.query(Subcategory).all():
                try:
                    num_id = int(sc.id.replace("subcat-", ""))
                    sc_id_lookup[num_id] = (sc.id, sc.name)
                except Exception:
                    pass

        # 5. Ingest Products
        products_csv = dataset_dir / "products.csv"
        prod_id_lookup = {}
        if products_csv.exists():
            df_p = pd.read_csv(products_csv)
            if db.query(Product).count() < len(df_p):
                db.query(Product).delete()
                prod_maps = []
                for _, row in df_p.iterrows():
                    p_id_num = int(row["ProductID"])
                    p_id_str = f"prod-{p_id_num}"
                    v_id_num = int(row["VendorID"])
                    c_id_num = int(row["CategoryID"])
                    sc_id_num = int(row["SubCategoryID"])
                    p_name = str(row["ProductName"])
                    price = float(row["Price"])

                    v_info = vendor_id_lookup.get(v_id_num, (f"vend-{v_id_num}", "Vendor Partner"))
                    c_info = cat_id_lookup.get(c_id_num, (f"cat-{c_id_num}", "Category"))
                    sc_info = sc_id_lookup.get(sc_id_num, (f"subcat-{sc_id_num}", "Subcategory"))

                    sku_val = f"SKU-{p_id_num:04d}"
                    prod_id_lookup[p_id_num] = (p_id_str, p_name, sku_val, price, v_info[0], v_info[1], c_info[1], "WatchSphere")

                    prod_maps.append({
                        "id": p_id_str,
                        "sku": sku_val,
                        "barcode": f"BAR-{p_id_num:06d}",
                        "name": p_name,
                        "brand": "WatchSphere",
                        "vendor_id": v_info[0],
                        "vendor_name": v_info[1],
                        "category_id": c_info[0],
                        "category_name": c_info[1],
                        "subcategory_id": sc_info[0],
                        "subcategory_name": sc_info[1],
                        "cost_price": round(price * 0.45, 2),
                        "selling_price": price,
                        "discount": float(row["Discount"]),
                        "profit_margin": 55.0,
                        "current_stock": int(row["Stock"]),
                        "minimum_stock": 5,
                        "warehouse": "WH-East Coast",
                        "status": "Active",
                        "rating": float(row["Rating"]),
                        "is_active": True
                    })
                db.bulk_insert_mappings(Product, prod_maps)
                db.commit()
                logger.info(f"Successfully imported {len(prod_maps)} Products into SQLite.")

        if not prod_id_lookup:
            for p in db.query(Product).all():
                try:
                    num_id = int(p.id.replace("prod-", ""))
                    prod_id_lookup[num_id] = (p.id, p.name, p.sku, p.selling_price, p.vendor_id, p.vendor_name, p.category_name, p.brand)
                except Exception:
                    pass

        # 6. Ingest Customers
        cust_csv = dataset_dir / "customers.csv"
        cust_id_lookup = {}
        if cust_csv.exists():
            df_cust = pd.read_csv(cust_csv)
            if db.query(Customer).count() < len(df_cust):
                db.query(Customer).delete()
                cust_maps = []
                for _, row in df_cust.iterrows():
                    c_id_num = int(row["CustomerID"])
                    c_id_str = f"cust-{c_id_num}"
                    c_name = str(row["Name"])
                    cust_id_lookup[c_id_num] = (c_id_str, c_name)
                    cust_maps.append({
                        "id": c_id_str,
                        "full_name": c_name,
                        "email": f"customer_{c_id_num}@watchsphere.ai",
                        "phone": f"+91 98{c_id_num:08d}",
                        "gender": str(row["Gender"]),
                        "age": int(row["Age"]),
                        "city": str(row["City"]),
                        "state": str(row["State"]),
                        "country": "India",
                        "segment": "Regular Consumer",
                        "status": "Active",
                        "orders_count": 0,
                        "total_spending": 0.0,
                        "avg_order_value": 0.0,
                        "last_purchase_date": str(row["RegistrationDate"]),
                        "is_active": True
                    })
                db.bulk_insert_mappings(Customer, cust_maps)
                db.commit()
                logger.info(f"Successfully imported {len(cust_maps)} Customers into SQLite.")

        if not cust_id_lookup:
            for c in db.query(Customer).all():
                try:
                    num_id = int(c.id.replace("cust-", ""))
                    cust_id_lookup[num_id] = (c.id, c.full_name)
                except Exception:
                    pass

        # 7. Ingest Orders
        orders_csv = dataset_dir / "orders.csv"
        ord_id_lookup = {}
        v_list = list(vendor_id_lookup.values()) if vendor_id_lookup else [("vend-1", "Acme Watch Co.")]
        if orders_csv.exists():
            df_ord = pd.read_csv(orders_csv)
            if db.query(Order).count() < len(df_ord):
                db.query(Order).delete()
                ord_maps = []
                for _, row in df_ord.iterrows():
                    o_id_num = int(row["OrderID"])
                    o_id_str = f"ord-{o_id_num}"
                    c_id_num = int(row["CustomerID"])
                    status = str(row["Status"])
                    tot_amt = float(row["TotalAmount"])
                    ord_date = str(row["OrderDate"])

                    c_info = cust_id_lookup.get(c_id_num, (f"cust-{c_id_num}", "Customer"))
                    v_info = v_list[o_id_num % len(v_list)]
                    ord_num = f"ORD-{o_id_num:06d}"
                    ord_id_lookup[o_id_num] = (o_id_str, ord_num, c_info[0], c_info[1], ord_date)

                    ord_maps.append({
                        "id": o_id_str,
                        "order_number": ord_num,
                        "customer_id": c_info[0],
                        "customer_name": c_info[1],
                        "vendor_id": v_info[0],
                        "vendor_name": v_info[1],
                        "items_count": 1,
                        "total_amount": tot_amt,
                        "discount_amount": 0.0,
                        "gst_amount": round(tot_amt * 0.18, 2),
                        "final_amount": tot_amt,
                        "payment_method": "Credit Card",
                        "payment_status": "Paid" if status in ["Completed", "Delivered", "Shipped"] else "Pending",
                        "order_status": status,
                        "order_date": ord_date,
                        "is_active": True
                    })
                db.bulk_insert_mappings(Order, ord_maps)
                db.commit()
                logger.info(f"Successfully imported {len(ord_maps)} Orders into SQLite.")

        if not ord_id_lookup:
            for o in db.query(Order).all():
                try:
                    num_id = int(o.id.replace("ord-", ""))
                    ord_id_lookup[num_id] = (o.id, o.order_number, o.customer_id, o.customer_name, o.order_date)
                except Exception:
                    pass

        # 8. Ingest Order Items
        oi_csv = dataset_dir / "order_items.csv"
        if oi_csv.exists() and db.query(OrderItem).count() < len(pd.read_csv(oi_csv)):
            df_oi = pd.read_csv(oi_csv)
            db.query(OrderItem).delete()
            oi_maps = []
            for _, row in df_oi.iterrows():
                oi_id_num = int(row["OrderItemID"])
                o_id_num = int(row["OrderID"])
                p_id_num = int(row["ProductID"])
                qty = int(row["Quantity"])
                unit_price = float(row["UnitPrice"])

                o_info = ord_id_lookup.get(o_id_num, (f"ord-{o_id_num}", f"ORD-{o_id_num:06d}", "cust-1", "Customer", "2026-01-01"))
                p_info = prod_id_lookup.get(p_id_num, (f"prod-{p_id_num}", "Watch Product", f"SKU-{p_id_num:04d}", unit_price, "vend-1", "Vendor", "Category", "Brand"))

                oi_maps.append({
                    "id": f"oi-{oi_id_num}",
                    "order_id": o_info[0],
                    "product_id": p_info[0],
                    "product_name": p_info[1],
                    "sku": p_info[2],
                    "unit_price": unit_price,
                    "quantity": qty,
                    "subtotal": round(qty * unit_price, 2),
                    "is_active": True
                })
            db.bulk_insert_mappings(OrderItem, oi_maps)
            db.commit()
            logger.info(f"Successfully imported {len(oi_maps)} Order Items into SQLite.")

        # 9. Ingest Payments
        pay_csv = dataset_dir / "payments.csv"
        if pay_csv.exists() and db.query(Payment).count() < len(pd.read_csv(pay_csv)):
            df_pay = pd.read_csv(pay_csv)
            db.query(Payment).delete()
            pay_maps = []
            for _, row in df_pay.iterrows():
                pay_id_num = int(row["PaymentID"])
                o_id_num = int(row["OrderID"])
                method = str(row["Method"])
                pay_status = str(row["PaymentStatus"])
                amt = float(row["Amount"])

                o_info = ord_id_lookup.get(o_id_num, (f"ord-{o_id_num}", f"ORD-{o_id_num:06d}", "cust-1", "Customer", "2026-01-01"))

                pay_maps.append({
                    "id": f"pay-{pay_id_num}",
                    "order_id": o_info[0],
                    "order_number": o_info[1],
                    "customer_id": o_info[2],
                    "customer_name": o_info[3],
                    "payment_method": method,
                    "transaction_id": f"TXN-{pay_id_num:06d}",
                    "gateway": "Stripe / Razorpay",
                    "amount": amt,
                    "status": pay_status,
                    "payment_date": o_info[4],
                    "is_active": True
                })
            db.bulk_insert_mappings(Payment, pay_maps)
            db.commit()
            logger.info(f"Successfully imported {len(pay_maps)} Payments into SQLite.")

        # 10. Ingest Reviews
        rev_csv = dataset_dir / "reviews.csv"
        if rev_csv.exists() and db.query(Review).count() < len(pd.read_csv(rev_csv)):
            df_rev = pd.read_csv(rev_csv)
            db.query(Review).delete()
            rev_maps = []
            for _, row in df_rev.iterrows():
                rev_id_num = int(row["ReviewID"])
                c_id_num = int(row["CustomerID"])
                p_id_num = int(row["ProductID"])
                rating = float(row["Rating"])
                text = str(row["Review"])

                c_info = cust_id_lookup.get(c_id_num, (f"cust-{c_id_num}", "Customer"))
                p_info = prod_id_lookup.get(p_id_num, (f"prod-{p_id_num}", "Watch Product", "SKU-001", 100.0, "vend-1", "Vendor Partner", "Category", "Brand"))

                rev_maps.append({
                    "id": f"rev-{rev_id_num}",
                    "customer_id": c_info[0],
                    "customer_name": c_info[1],
                    "product_id": p_info[0],
                    "product_name": p_info[1],
                    "vendor_id": p_info[4],
                    "vendor_name": p_info[5],
                    "rating": rating,
                    "title": "Customer Review",
                    "review_text": text,
                    "sentiment": "Positive" if rating >= 4.0 else ("Neutral" if rating >= 3.0 else "Negative"),
                    "status": "Approved",
                    "is_active": True
                })
            db.bulk_insert_mappings(Review, rev_maps)
            db.commit()
            logger.info(f"Successfully imported {len(rev_maps)} Reviews into SQLite.")

        # 11. Ingest Wishlist
        wish_csv = dataset_dir / "wishlist.csv"
        if wish_csv.exists() and db.query(Wishlist).count() < len(pd.read_csv(wish_csv)):
            df_wish = pd.read_csv(wish_csv)
            db.query(Wishlist).delete()
            wish_maps = []
            for _, row in df_wish.iterrows():
                w_id_num = int(row["WishlistID"])
                c_id_num = int(row["CustomerID"])
                p_id_num = int(row["ProductID"])

                c_info = cust_id_lookup.get(c_id_num, (f"cust-{c_id_num}", "Customer"))
                p_info = prod_id_lookup.get(p_id_num, (f"prod-{p_id_num}", "Watch Product", "SKU-001", 100.0, "vend-1", "Vendor Partner", "Category", "Brand"))

                wish_maps.append({
                    "id": f"wish-{w_id_num}",
                    "customer_id": c_info[0],
                    "customer_name": c_info[1],
                    "product_id": p_info[0],
                    "product_name": p_info[1],
                    "category": p_info[6],
                    "brand": p_info[7],
                    "status": "Active",
                    "is_active": True
                })
            db.bulk_insert_mappings(Wishlist, wish_maps)
            db.commit()
            logger.info(f"Successfully imported {len(wish_maps)} Wishlist records into SQLite.")

        # 12. Ingest Product Images
        img_csv = dataset_dir / "product_images.csv"
        if img_csv.exists() and db.query(ProductImage).count() < len(pd.read_csv(img_csv)):
            df_img = pd.read_csv(img_csv)
            db.query(ProductImage).delete()
            img_maps = []
            for _, row in df_img.iterrows():
                p_id_num = int(row["ProductID"])
                img_url = str(row["ImageURL"])
                p_info = prod_id_lookup.get(p_id_num, (f"prod-{p_id_num}", "Watch Product", "SKU-001", 100.0, "vend-1", "Vendor Partner", "Category", "Brand"))

                img_maps.append({
                    "id": f"img-{p_id_num}",
                    "product_id": p_info[0],
                    "image_url": img_url,
                    "is_thumbnail": True,
                    "is_active": True
                })
            db.bulk_insert_mappings(ProductImage, img_maps)
            db.commit()
            logger.info(f"Successfully imported {len(img_maps)} Product Images into SQLite.")

        elapsed = time.time() - start_time
        logger.info(f"WatchSphere Master datasets successfully imported into SQLite in {elapsed:.2f} seconds.")

    except Exception as e:
        logger.error(f"Auto-seed error: {str(e)}")
        db.rollback()
    finally:
        db.close()


def seed_database_from_datasets():
    auto_seed_datasets()


if __name__ == "__main__":
    auto_seed_datasets()

