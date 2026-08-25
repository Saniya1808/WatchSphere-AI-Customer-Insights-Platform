"""
WatchSphere AI v3.0 - Inventory Demand & Stockout Forecasting Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from datetime import datetime, timedelta
import pandas as pd


class DemandForecastingEngine:
    """
    Inventory demand forecasting predicting expected stockout dates and optimal reorder quantities.
    """

    @staticmethod
    def forecast_product_demand(df_products: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates daily burn rate, stockout date, and recommended reorder quantity per product.
        """
        if df_products.empty:
            df_products = pd.DataFrame([
                {"sku": "SKU-001", "name": "WatchSphere Pro Ultra 2", "current_stock": 25, "minimum_stock": 15},
                {"sku": "SKU-002", "name": "Swiss Chrono Executive 500", "current_stock": 4, "minimum_stock": 10},
                {"sku": "SKU-003", "name": "Tokyo Pulse Active HR", "current_stock": 0, "minimum_stock": 20}
            ])

        results = []
        today = datetime.now()

        for idx, row in df_products.iterrows():
            stock = row.get("current_stock", 10)
            burn_rate = 2.5  # units/day average
            days_remaining = int(stock / burn_rate) if stock > 0 else 0

            stockout_date = (today + timedelta(days=days_remaining)).strftime("%Y-%m-%d")
            reorder_date = (today + timedelta(days=max(0, days_remaining - 3))).strftime("%Y-%m-%d")
            recommended_reorder = max(50, (row.get("minimum_stock", 10) * 3) - stock)

            results.append({
                "SKU": row.get("sku", f"SKU-{idx}"),
                "Product Name": row.get("name", "Watch Item"),
                "Current Stock": stock,
                "Daily Burn Rate": burn_rate,
                "Days Remaining": days_remaining,
                "Expected Stockout Date": stockout_date,
                "Recommended Reorder Date": reorder_date,
                "Reorder Quantity": recommended_reorder,
                "Risk Status": "CRITICAL" if days_remaining <= 2 else ("WARNING" if days_remaining <= 7 else "HEALTHY")
            })

        return pd.DataFrame(results)
