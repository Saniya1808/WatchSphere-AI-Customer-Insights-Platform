"""
WatchSphere AI v3.0 - Dynamic Price Optimization Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import numpy as np
import pandas as pd


class PriceOptimizationEngine:
    """
    Dynamic price optimization model maximizing profit margin based on price elasticity of demand.
    """

    @staticmethod
    def optimize_price(cost_price: float, current_price: float) -> dict:
        """
        Calculates price-demand elasticity curve and determines optimal selling price.
        """
        prices = np.linspace(cost_price * 1.1, current_price * 1.5, 20)
        # Elasticity curve: Q = A * (P ^ -elasticity)
        elasticity = 1.8
        base_demand = 1500

        demands = base_demand * ((prices / current_price) ** -elasticity)
        revenues = prices * demands
        profits = (prices - cost_price) * demands

        opt_idx = np.argmax(profits)
        suggested_price = round(float(prices[opt_idx]), 2)
        expected_profit = round(float(profits[opt_idx]), 2)
        expected_sales = int(demands[opt_idx])

        curve_df = pd.DataFrame({
            "price": np.round(prices, 2),
            "predicted_sales": np.round(demands, 0),
            "expected_revenue": np.round(revenues, 2),
            "expected_profit": np.round(profits, 2)
        })

        return {
            "current_price": current_price,
            "cost_price": cost_price,
            "suggested_price": suggested_price,
            "expected_profit": expected_profit,
            "expected_sales": expected_sales,
            "profit_lift_pct": round(((expected_profit - ((current_price - cost_price) * demands[10])) / max(1, (current_price - cost_price) * demands[10])) * 100, 2),
            "curve_df": curve_df
        }
