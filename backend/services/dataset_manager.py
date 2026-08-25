"""
WatchSphere AI v3.0 - Dataset Manager Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
from config.logging import logger

DATASETS_DIR = Path("datasets")


class DatasetManager:
    """
    Scans, inspects, and detects dataset files inside `datasets/` folder.
    """

    KNOWN_DATASETS = [
        "Customers", "Orders", "Products", "Categories", "Subcategories",
        "Payments", "Reviews", "Inventory", "Sales", "Forecast",
        "Recommendations", "Wishlist", "Cart", "Vendor", "Warehouse",
        "Customer Activity", "Dashboard Summary", "Monthly Sales",
        "Yearly Sales", "Category Sales", "Vendor Sales", "Sales Summary"
    ]

    @staticmethod
    def get_all_dataset_status() -> List[Dict[str, Any]]:
        """
        Scans datasets directory and returns status metadata cards for all 22 expected datasets.
        """
        DATASETS_DIR.mkdir(parents=True, exist_ok=True)
        results = []

        for ds_name in DatasetManager.KNOWN_DATASETS:
            file_key = ds_name.lower().replace(" ", "_")
            csv_path = DATASETS_DIR / f"{file_key}.csv"
            xlsx_path = DATASETS_DIR / f"{file_key}.xlsx"

            target_path = csv_path if csv_path.exists() else (xlsx_path if xlsx_path.exists() else None)

            if target_path and target_path.exists():
                try:
                    df = pd.read_csv(target_path) if target_path.suffix == ".csv" else pd.read_excel(target_path)
                    rows, cols = df.shape
                    size_bytes = target_path.stat().st_size
                    size_str = f"{size_bytes / 1024:.1f} KB" if size_bytes < 1024 * 1024 else f"{size_bytes / (1024*1024):.2f} MB"
                    mtime = datetime.fromtimestamp(target_path.stat().st_mtime).strftime("%b %d, %H:%M")
                    status = "Loaded & Synced"
                except Exception as e:
                    logger.warning(f"Error inspecting dataset {target_path}: {e}")
                    rows, cols = 0, 0
                    size_str = "0 KB"
                    mtime = "N/A"
                    status = "Error"
            else:
                rows, cols = 0, 0
                size_str = "0 KB"
                mtime = "N/A"
                status = "Not Found"

            results.append({
                "dataset_name": ds_name,
                "file_key": file_key,
                "rows": rows,
                "columns": cols,
                "file_size": size_str,
                "status": status,
                "last_updated": mtime
            })

        return results
