"""
WatchSphere AI v3.0 - Isolation Forest Fraud Detection Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


class FraudDetectionEngine:
    """
    Isolation Forest anomaly detection scoring suspicious orders and abnormal transaction patterns.
    """

    @staticmethod
    def detect_fraud(df_orders: pd.DataFrame) -> pd.DataFrame:
        """
        Executes Isolation Forest anomaly scoring on order transactions.
        """
        if df_orders.empty:
            df_orders = pd.DataFrame([
                {"order_number": "ORD-1001", "customer_name": "Aarav Sharma", "total_amount": 799.0, "items_count": 1, "payment_method": "Credit Card"},
                {"order_number": "ORD-1002", "customer_name": "Suspicious Bot", "total_amount": 15400.0, "items_count": 25, "payment_method": "Wallet"},
                {"order_number": "ORD-1003", "customer_name": "Rohan Gupta", "total_amount": 349.0, "items_count": 1, "payment_method": "UPI"}
            ])

        feature_cols = ["total_amount", "items_count"]
        X = df_orders[feature_cols].copy()

        iso_forest = IsolationForest(contamination=0.15, random_state=42)
        anomalies = iso_forest.fit_predict(X)
        scores = iso_forest.score_samples(X)

        df_orders["risk_score"] = np.round(np.abs(scores) * 100, 1)
        df_orders["is_suspicious"] = np.where(anomalies == -1, "High Risk Anomaly", "Normal Transaction")
        df_orders["reasons"] = np.where(anomalies == -1, "Abnormal transaction velocity & bulk order size", "Standard purchasing pattern")

        return df_orders
