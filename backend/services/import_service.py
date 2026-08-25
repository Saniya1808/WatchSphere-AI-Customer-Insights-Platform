"""
WatchSphere AI v3.0 - Data Import & Ingestion Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from pathlib import Path
from typing import Tuple
import pandas as pd
from config.logging import logger

DATASETS_DIR = Path("datasets")


class ImportService:
    """
    Handles CSV and Excel data ingestion into datasets/ storage and triggers dashboard refresh.
    """

    @staticmethod
    def import_dataset(
        df: pd.DataFrame,
        target_dataset_name: str,
        mode: str = "Append Data"
    ) -> Tuple[bool, str]:
        """
        Imports uploaded DataFrame into datasets/<target>.csv.
        Modes: 'Append Data', 'Replace Existing Data', 'Skip Duplicate Records'
        """
        DATASETS_DIR.mkdir(parents=True, exist_ok=True)
        file_key = target_dataset_name.lower().replace(" ", "_")
        csv_path = DATASETS_DIR / f"{file_key}.csv"

        try:
            if mode == "Replace Existing Data" or not csv_path.exists():
                final_df = df
            else:
                existing_df = pd.read_csv(csv_path)
                if mode == "Skip Duplicate Records":
                    combined_df = pd.concat([existing_df, df], ignore_index=True)
                    final_df = combined_df.drop_duplicates()
                else:  # Append Data
                    final_df = pd.concat([existing_df, df], ignore_index=True)

            final_df.to_csv(csv_path, index=False)
            logger.info(f"Successfully imported {len(df)} rows into '{csv_path.name}' using mode '{mode}'. Total rows: {len(final_df)}.")
            return True, f"Successfully imported {len(df)} records into '{target_dataset_name}' ({len(final_df)} total rows)."
        except Exception as e:
            logger.error(f"Error importing dataset '{target_dataset_name}': {str(e)}")
            return False, f"Import failed: {str(e)}"
