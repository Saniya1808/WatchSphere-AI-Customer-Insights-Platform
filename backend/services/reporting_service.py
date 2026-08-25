"""
WatchSphere AI v3.0 - Enterprise Reporting Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import List, Dict, Any
import pandas as pd
from backend.services.catalog_export_service import CatalogExportService


class ReportingService:
    """
    Generates enterprise executive reports across 13 domains in PDF, Excel, CSV, and HTML formats.
    """

    REPORT_DOMAINS = [
        "Sales Report", "Revenue Report", "Customer Report", "Vendor Report",
        "Inventory Report", "Product Report", "Payment Report", "Review Report",
        "AI Prediction Report", "Forecast Report", "Churn Report", "Fraud Report", "Recommendation Report"
    ]

    @staticmethod
    def generate_report_bytes(domain: str, fmt: str, data: List[Dict[str, Any]]) -> tuple[bytes, str]:
        """
        Generates formatted report payload bytes and filename.
        """
        clean_name = domain.lower().replace(" ", "_")

        if not data:
            data = [{"Report": domain, "Status": "No records found", "Generated_At": "2026-08-06"}]

        if fmt == "CSV":
            csv_str = CatalogExportService.export_to_csv(data)
            return csv_str.encode("utf-8"), f"{clean_name}.csv"
        elif fmt == "Excel":
            excel_b = CatalogExportService.export_to_excel_bytes(data)
            return excel_b, f"{clean_name}.xlsx"
        elif fmt == "HTML":
            df = pd.DataFrame(data)
            html_str = f"<h2>WatchSphere AI — {domain}</h2>" + df.to_html()
            return html_str.encode("utf-8"), f"{clean_name}.html"
        else:  # PDF (Simulated PDF document layout)
            df = pd.DataFrame(data)
            pdf_str = f"==============================================\nWATCHSPHERE AI v3.0 — EXECUTIVE {domain.upper()}\n==============================================\n" + df.to_string()
            return pdf_str.encode("utf-8"), f"{clean_name}.pdf"
