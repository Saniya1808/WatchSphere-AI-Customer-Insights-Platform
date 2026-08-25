"""
WatchSphere AI v3.0 - Executive Analytics Data Aggregation Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any
import pandas as pd


class AnalyticsService:
    """
    Data aggregation engine preparing structured DataFrames for Plotly chart suite.
    """

    @staticmethod
    def get_monthly_revenue_trend(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Monthly revenue & order count aggregation."""
        if df_orders.empty:
            return pd.DataFrame(columns=["Month", "Revenue", "Orders"])

        date_col = next((c for c in ["OrderDate", "order_date", "date"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        id_col = next((c for c in ["OrderID", "order_id", "order_number"] if c in df_orders.columns), df_orders.columns[0])

        if not date_col or not rev_col:
            return pd.DataFrame(columns=["Month", "Revenue", "Orders"])

        df = df_orders.copy()
        df["Month"] = pd.to_datetime(df[date_col], errors="coerce").dt.strftime("%Y-%m")
        grouped = df.groupby("Month").agg(
            Revenue=(rev_col, "sum"),
            Orders=(id_col, "count")
        ).reset_index().sort_values("Month")
        return grouped

    @staticmethod
    def get_revenue_by_category(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Revenue grouped by category."""
        cat_col = next((c for c in ["Category", "category", "CategoryName", "category_name"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        if df_orders.empty or not cat_col or not rev_col:
            return pd.DataFrame(columns=["category", "total_revenue"])
        return df_orders.groupby(cat_col)[rev_col].sum().reset_index().rename(columns={cat_col: "category", rev_col: "total_revenue"}).sort_values("total_revenue", ascending=False)

    @staticmethod
    def get_revenue_by_vendor(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Revenue grouped by vendor."""
        v_col = next((c for c in ["Vendor", "vendor_name", "CompanyName", "vendor"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        if df_orders.empty or not v_col or not rev_col:
            return pd.DataFrame(columns=["vendor_name", "total_revenue"])
        return df_orders.groupby(v_col)[rev_col].sum().reset_index().rename(columns={v_col: "vendor_name", rev_col: "total_revenue"}).sort_values("total_revenue", ascending=True)

    @staticmethod
    def get_revenue_by_city(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Revenue grouped by city."""
        city_col = next((c for c in ["City", "city"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        if df_orders.empty or not city_col or not rev_col:
            return pd.DataFrame(columns=["city", "total_revenue"])
        return df_orders.groupby(city_col)[rev_col].sum().reset_index().rename(columns={city_col: "city", rev_col: "total_revenue"}).sort_values("total_revenue", ascending=False)

    @staticmethod
    def get_revenue_by_payment_method(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Revenue grouped by payment method."""
        p_col = next((c for c in ["Method", "payment_method"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        if df_orders.empty or not p_col or not rev_col:
            return pd.DataFrame(columns=["payment_method", "total_revenue"])
        return df_orders.groupby(p_col)[rev_col].sum().reset_index().rename(columns={p_col: "payment_method", rev_col: "total_revenue"})

    @staticmethod
    def get_top_products(df_orders: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """Top N revenue generating products."""
        p_col = next((c for c in ["ProductName", "product_name", "Product"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        if df_orders.empty or not p_col or not rev_col:
            return pd.DataFrame(columns=["product_name", "total_revenue"])
        return df_orders.groupby(p_col)[rev_col].sum().reset_index().rename(columns={p_col: "product_name", rev_col: "total_revenue"}).sort_values("total_revenue", ascending=False).head(top_n)

    @staticmethod
    def get_bottom_products(df_orders: pd.DataFrame, bottom_n: int = 10) -> pd.DataFrame:
        """Bottom N lowest revenue generating products."""
        p_col = next((c for c in ["ProductName", "product_name", "Product"] if c in df_orders.columns), None)
        rev_col = next((c for c in ["TotalAmount", "total_revenue", "final_amount", "Revenue"] if c in df_orders.columns), None)
        if df_orders.empty or not p_col or not rev_col:
            return pd.DataFrame(columns=["product_name", "total_revenue"])
        return df_orders.groupby(p_col)[rev_col].sum().reset_index().rename(columns={p_col: "product_name", rev_col: "total_revenue"}).sort_values("total_revenue", ascending=True).head(bottom_n)

    @staticmethod
    def get_order_status_distribution(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Order status counts."""
        s_col = next((c for c in ["Status", "order_status"] if c in df_orders.columns), None)
        if df_orders.empty or not s_col:
            return pd.DataFrame(columns=["order_status", "count"])
        return df_orders[s_col].value_counts().reset_index(name="count").rename(columns={s_col: "order_status"})

    @staticmethod
    def get_payment_status_distribution(df_orders: pd.DataFrame) -> pd.DataFrame:
        """Payment status counts."""
        ps_col = next((c for c in ["PaymentStatus", "payment_status"] if c in df_orders.columns), None)
        if df_orders.empty or not ps_col:
            return pd.DataFrame(columns=["payment_status", "count"])
        return df_orders[ps_col].value_counts().reset_index(name="count").rename(columns={ps_col: "payment_status"})

    @staticmethod
    def get_inventory_by_warehouse(df_inventory: pd.DataFrame) -> pd.DataFrame:
        """Inventory value aggregated by warehouse."""
        w_col = next((c for c in ["Warehouse", "warehouse"] if c in df_inventory.columns), None)
        if df_inventory.empty or not w_col:
            return pd.DataFrame(columns=["warehouse", "inventory_value"])
        if "inventory_value" in df_inventory.columns:
            val_col = "inventory_value"
        elif "AvailableStock" in df_inventory.columns:
            df = df_inventory.copy()
            df["inventory_value"] = df["AvailableStock"] * 45.0
            val_col = "inventory_value"
        else:
            return pd.DataFrame(columns=["warehouse", "inventory_value"])
        return df_inventory.groupby(w_col)[val_col].sum().reset_index().rename(columns={w_col: "warehouse"})

