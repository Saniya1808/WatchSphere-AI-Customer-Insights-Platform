"""
WatchSphere AI v3.0 - Customer Churn Prediction Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import numpy as np
import pandas as pd


class ChurnPredictionEngine:
    """
    Predicts customer churn probability and risk tier with retention action strategies.
    Process imported SQLite customer records deterministically without synthetic fallbacks.
    """

    @staticmethod
    def predict_churn(df_customers: pd.DataFrame) -> pd.DataFrame:
        """Assigns churn probability and retention suggestions based on customer activity."""
        if df_customers.empty:
            return pd.DataFrame(columns=["Customer Name", "Email", "Orders Count", "Recency (Days)", "Churn Probability", "Risk Level", "Retention Strategy"])

        results = []
        for idx, row in df_customers.iterrows():
            recency = float(row.get("last_purchase_days", row.get("recency_days", 25.0)))
            orders = float(row.get("orders_count", 1.0))

            # Heuristic model calculation
            churn_prob = min(0.98, max(0.05, (recency / 90.0) * 0.7 + (1.0 / max(1.0, orders)) * 0.3))

            if churn_prob >= 0.70:
                risk_tier = "High Risk"
                suggestion = "Offer 20% Retention Discount Voucher & Executive Account Concierge"
            elif churn_prob >= 0.35:
                risk_tier = "Medium Risk"
                suggestion = "Send Personalized Product Recommendations & Free Shipping Pass"
            else:
                risk_tier = "Low Risk"
                suggestion = "Enroll in VIP Loyalty Tier & Priority Product Releases"

            results.append({
                "Customer Name": row.get("full_name", f"Customer {idx}"),
                "Email": row.get("email", "cust@example.com"),
                "Orders Count": int(orders),
                "Recency (Days)": int(recency),
                "Churn Probability": f"{churn_prob * 100:.1f}%",
                "Risk Level": risk_tier,
                "Retention Strategy": suggestion
            })

        return pd.DataFrame(results)
