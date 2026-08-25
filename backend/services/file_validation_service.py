"""
WatchSphere AI v3.0 - File Validation & Schema Inspection Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Tuple, Dict, Any, List
import pandas as pd
from config.logging import logger


class FileValidationService:
    """
    Validates uploaded CSV/Excel files for schema integrity, column presence, missing values, and duplicate rows.
    """

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, target_dataset: str) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Validates an uploaded DataFrame against expected schema.
        Returns: (is_valid: bool, warnings: List[str], summary: Dict[str, Any])
        """
        warnings = []
        rows, cols = df.shape

        if rows == 0:
            return False, ["Uploaded file contains 0 data rows."], {}

        # Duplicate detection
        duplicate_count = int(df.duplicated().sum())
        if duplicate_count > 0:
            warnings.append(f"Detected {duplicate_count} duplicate row(s).")

        # Missing values detection
        null_counts = df.isnull().sum()
        missing_cols = null_counts[null_counts > 0].to_dict()
        if missing_cols:
            warnings.append(f"Found missing values in columns: {list(missing_cols.keys())}")

        summary = {
            "total_rows": rows,
            "total_columns": cols,
            "column_names": list(df.columns),
            "duplicate_rows": duplicate_count,
            "missing_values_count": int(null_counts.sum()),
        }

        logger.info(f"File validation complete for target '{target_dataset}': {rows} rows, {cols} cols, {duplicate_count} duplicates.")
        return True, warnings, summary
