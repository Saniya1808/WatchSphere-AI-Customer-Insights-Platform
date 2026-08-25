"""
WatchSphere AI v3.0 - Catalog Import & Export Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Dict, Any, Tuple
import io
import pandas as pd
from config.logging import logger


class CatalogExportService:
    """
    Generates CSV and Excel downloads for Vendor and Product catalogs and handles bulk CSV/Excel imports.
    """

    @staticmethod
    def export_to_csv(data_dicts: List[Dict[str, Any]]) -> str:
        """Converts list of entity dictionaries into CSV string."""
        if not data_dicts:
            return ""
        df = pd.DataFrame(data_dicts)
        return df.to_csv(index=False)

    @staticmethod
    def export_to_excel_bytes(data_dicts: List[Dict[str, Any]]) -> bytes:
        """Converts list of entity dictionaries into Excel (.xlsx) file bytes."""
        if not data_dicts:
            return b""
        df = pd.DataFrame(data_dicts)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Catalog Export")
        return output.getvalue()
