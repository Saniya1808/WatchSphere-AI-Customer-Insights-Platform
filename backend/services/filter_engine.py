"""
WatchSphere AI v3.0 - Multi-Dimensional Global Filter Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any, Tuple, List
import pandas as pd


class FilterEngine:
    """
    Applies multi-dimensional filtering across Orders, Products, and Inventory data streams.
    """

    @staticmethod
    def apply_filters(
        df_orders: pd.DataFrame,
        filters: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Applies filter state parameters to Orders DataFrame.
        Supported filters:
        - date_range (tuple: start_date, end_date)
        - vendor (str or 'All Vendors')
        - brand (str or 'All Brands')
        - category (str or 'All Categories')
        - sub_category (str or 'All Subcategories')
        - order_status (str or 'All Statuses')
        - payment_status (str or 'All Statuses')
        - city (str or 'All Cities')
        - state (str or 'All States')
        - country (str or 'All Countries')
        - warehouse (str or 'All Warehouses')
        - customer_segment (str or 'All Segments')
        """
        if df_orders.empty:
            return df_orders

        filtered_df = df_orders.copy()

        # Date Range Filter
        date_range = filters.get("date_range")
        if date_range and len(date_range) == 2 and "order_date" in filtered_df.columns:
            start_d, end_d = date_range
            filtered_df["_dt"] = pd.to_datetime(filtered_df["order_date"], errors="coerce")
            filtered_df = filtered_df[
                (filtered_df["_dt"].dt.date >= start_d) &
                (filtered_df["_dt"].dt.date <= end_d)
            ].drop(columns=["_dt"], errors="ignore")

        # Generic Categorical Filters Map
        filter_map = {
            "vendor": "vendor_name",
            "brand": "brand",
            "category": "category",
            "sub_category": "sub_category",
            "order_status": "order_status",
            "payment_status": "payment_status",
            "city": "city",
            "country": "country",
            "warehouse": "warehouse",
            "customer_segment": "customer_segment"
        }

        for param_key, col_name in filter_map.items():
            val = filters.get(param_key)
            if val and val != "All" and not str(val).startswith("All ") and col_name in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col_name].astype(str) == str(val)]

        return filtered_df
