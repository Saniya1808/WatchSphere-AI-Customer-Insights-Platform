"""
WatchSphere AI v3.0 - Commerce Analytics Data Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any
import pandas as pd


class CommerceAnalyticsService:
    """
    Computes data aggregations for Customer Analytics Dashboard tab.
    """

    @staticmethod
    def get_customer_geo_distribution(df_customers: pd.DataFrame) -> pd.DataFrame:
        if df_customers.empty or "city" not in df_customers.columns:
            return pd.DataFrame(columns=["city", "count"])
        return df_customers["city"].value_counts().reset_index(name="count")

    @staticmethod
    def get_gender_distribution(df_customers: pd.DataFrame) -> pd.DataFrame:
        if df_customers.empty or "gender" not in df_customers.columns:
            return pd.DataFrame(columns=["gender", "count"])
        return df_customers["gender"].value_counts().reset_index(name="count")

    @staticmethod
    def get_segment_distribution(df_customers: pd.DataFrame) -> pd.DataFrame:
        if df_customers.empty or "segment" not in df_customers.columns:
            return pd.DataFrame(columns=["segment", "count"])
        return df_customers["segment"].value_counts().reset_index(name="count")

    @staticmethod
    def get_clv_distribution(df_customers: pd.DataFrame) -> pd.DataFrame:
        if df_customers.empty or "total_spending" not in df_customers.columns:
            return pd.DataFrame(columns=["full_name", "total_spending"])
        return df_customers.sort_values("total_spending", ascending=False).head(10)[["full_name", "total_spending"]]
