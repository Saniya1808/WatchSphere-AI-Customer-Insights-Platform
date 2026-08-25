"""
WatchSphere AI v3.0 - Enterprise AI & Machine Learning Engine Unit Tests (Phase 6)
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import pandas as pd
from ml.preprocessing import MLPreprocessingPipeline
from ml.customer_segmentation import CustomerSegmentationEngine
from ml.recommendation_engine import HybridRecommendationEngine
from ml.sentiment_analysis import SentimentAnalysisEngine
from ml.sales_forecasting import SalesForecastingEngine
from ml.demand_forecasting import DemandForecastingEngine
from ml.churn_prediction import ChurnPredictionEngine
from ml.price_optimization import PriceOptimizationEngine
from ml.fraud_detection import FraudDetectionEngine
from ml.model_registry import ModelRegistryManager
from backend.services.ai_service import AIService


def test_customer_segmentation():
    """Test KMeans clustering and 2D/3D PCA projection."""
    df_cust = pd.DataFrame({
        "full_name": [f"Cust {i}" for i in range(10)],
        "age": [25, 45, 35, 50, 22, 60, 30, 40, 55, 28],
        "orders_count": [10, 2, 15, 1, 8, 3, 12, 5, 2, 7],
        "total_spending": [2500, 150, 4200, 50, 1800, 300, 3100, 800, 200, 1500],
        "recency_days": [5, 60, 2, 85, 12, 45, 8, 30, 70, 15]
    })
    res = CustomerSegmentationEngine.run_segmentation(df_cust, n_clusters=3)
    assert "df_segmented" in res
    assert "silhouette_score" in res
    assert "persona" in res["df_segmented"].columns


def test_hybrid_recommendation():
    """Test Hybrid Product Recommender."""
    res = HybridRecommendationEngine.get_recommendations("SKU-001", pd.DataFrame())
    assert len(res["recommendations"]) > 0
    assert "precision_at_k" in res["metrics"]


def test_sentiment_analysis():
    """Test NLP sentiment analysis text classifier."""
    pos_res = SentimentAnalysisEngine.analyze_text("This watch is amazing and outstanding quality!")
    assert pos_res["sentiment"] == "Positive"
    assert pos_res["confidence"] > 0.70

    neg_res = SentimentAnalysisEngine.analyze_text("Terrible product, broken and worst customer service.")
    assert neg_res["sentiment"] == "Negative"


def test_sales_forecasting():
    """Test 30-day time series revenue forecasting."""
    res = SalesForecastingEngine.forecast_sales(30)
    assert res["days_ahead"] == 30
    assert res["total_forecasted_revenue"] > 0
    assert "predicted_revenue" in res["forecast_df"].columns


def test_demand_forecasting():
    """Test inventory demand and stockout predictions."""
    df_prd = pd.DataFrame([{"sku": "SKU-001", "name": "Watch A", "current_stock": 5, "minimum_stock": 10}])
    df_demand = DemandForecastingEngine.forecast_product_demand(df_prd)
    assert len(df_demand) == 1
    assert "Expected Stockout Date" in df_demand.columns


def test_churn_prediction():
    """Test customer churn risk tiering."""
    df_cust = pd.DataFrame([{"full_name": "Aarav", "email": "aarav@test.com", "orders_count": 1, "last_purchase_days": 80}])
    df_churn = ChurnPredictionEngine.predict_churn(df_cust)
    assert "Churn Probability" in df_churn.columns
    assert "Risk Level" in df_churn.columns


def test_price_optimization():
    """Test price elasticity profit curve optimizer."""
    res = PriceOptimizationEngine.optimize_price(350.0, 799.0)
    assert res["suggested_price"] > 350.0
    assert "expected_profit" in res


def test_fraud_detection():
    """Test Isolation Forest anomaly scoring."""
    df_orders = pd.DataFrame([
        {"order_number": "O-1", "total_amount": 100.0, "items_count": 1},
        {"order_number": "O-2", "total_amount": 99999.0, "items_count": 50}
    ])
    df_fraud = FraudDetectionEngine.detect_fraud(df_orders)
    assert "is_suspicious" in df_fraud.columns


def test_model_registry_and_service(db_session):
    """Test AI Model Registry and Service."""
    ai_service = AIService(db_session)
    models = ai_service.get_registered_models()
    assert len(models) >= 5
    ok, msg = ai_service.retrain_model(models[0]["name"])
    assert ok is True
