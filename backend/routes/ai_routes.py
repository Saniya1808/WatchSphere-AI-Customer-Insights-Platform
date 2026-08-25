"""
WatchSphere AI v3.0 - Machine Learning & Artificial Intelligence API Routes
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.response_schema import APIResponse
from backend.services.ai_service import AIService
from ml.sales_forecasting import SalesForecastingEngine
from ml.demand_forecasting import DemandForecastingEngine
from ml.customer_segmentation import CustomerSegmentationEngine
from ml.recommendation_engine import HybridRecommendationEngine
from ml.sentiment_analysis import SentimentAnalysisEngine
from ml.fraud_detection import FraudDetectionEngine
from ml.price_optimization import PriceOptimizationEngine
from backend.models.product import Product
from backend.models.customer import Customer
from backend.models.order import Order

router = APIRouter(prefix="/ml", tags=["Machine Learning AI Engines"])


@router.get("/models", summary="List Registered AI Models")
def list_ai_models(db: Session = Depends(get_db)):
    service = AIService(db)
    models = service.get_registered_models()
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message=f"Retrieved {len(models)} registered ML models",
        data=models
    )


@router.get("/forecast/sales", summary="Run AI Sales Revenue Forecast")
def run_sales_forecast(periods: int = Query(30, description="Forecast horizon in days")):
    try:
        result = SalesForecastingEngine.forecast_sales(days_ahead=periods)
        if "forecast_df" in result and isinstance(result["forecast_df"], pd.DataFrame):
            result["forecast_data"] = result["forecast_df"].to_dict(orient="records")
            del result["forecast_df"]
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message=f"Generated {periods} days of AI sales forecast",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sales forecast error: {str(e)}")


@router.get("/forecast/demand", summary="Run Product Demand Forecast")
def run_demand_forecast(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        df_prod = pd.DataFrame([{"sku": p.sku, "name": p.name, "category_name": p.category_name, "current_stock": p.current_stock} for p in products])
        result = DemandForecastingEngine.forecast_product_demand(df_prod)
        if isinstance(result, dict) and "demand_df" in result and isinstance(result["demand_df"], pd.DataFrame):
            result["demand_data"] = result["demand_df"].to_dict(orient="records")
            del result["demand_df"]
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="Generated product demand predictions",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demand forecast error: {str(e)}")


@router.get("/segmentation", summary="Run Customer AI KMeans Clustering")
def run_customer_segmentation(n_clusters: int = Query(4, description="Number of clusters"), db: Session = Depends(get_db)):
    try:
        customers = db.query(Customer).all()
        df_cust = pd.DataFrame([{"id": c.id, "full_name": c.full_name, "age": c.age or 30, "orders_count": c.orders_count, "total_spending": c.total_spending, "recency_days": 15} for c in customers])
        result = CustomerSegmentationEngine.run_segmentation(df_cust, n_clusters=n_clusters)
        if "df_segmented" in result and isinstance(result["df_segmented"], pd.DataFrame):
            result["segmented_customers"] = result["df_segmented"].head(50).to_dict(orient="records")
            del result["df_segmented"]
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message=f"Clustered customer dataset into {n_clusters} segments",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer segmentation error: {str(e)}")


@router.get("/recommendations/{target_sku}", summary="Get Hybrid Product Recommendations")
def get_recommendations(target_sku: str, top_n: int = Query(5, description="Number of recommendations"), db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        df_prod = pd.DataFrame([{"sku": p.sku, "name": p.name, "brand": p.brand, "category_name": p.category_name, "selling_price": p.selling_price} for p in products])
        result = HybridRecommendationEngine.get_recommendations(target_product_sku=target_sku, df_products=df_prod, top_n=top_n)
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message=f"Generated recommendations for product SKU {target_sku}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation engine error: {str(e)}")


@router.get("/fraud-detection", summary="Run Isolation Forest Fraud Detection")
def run_fraud_detection(db: Session = Depends(get_db)):
    try:
        orders = db.query(Order).all()
        df_ord = pd.DataFrame([{"order_number": o.order_number, "customer_name": o.customer_name, "total_amount": o.total_amount, "items_count": o.items_count or 1, "payment_method": o.payment_method} for o in orders])
        fraud_df = FraudDetectionEngine.detect_fraud(df_ord)
        records = fraud_df.head(50).to_dict(orient="records") if isinstance(fraud_df, pd.DataFrame) else []
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message=f"Scanned order transactions and flagged anomalies",
            data=records
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fraud detection error: {str(e)}")


@router.get("/price-optimization/{product_id}", summary="Run Price Elasticity Optimization")
def run_price_optimization(product_id: str, db: Session = Depends(get_db)):
    try:
        prod = db.query(Product).filter(Product.id == product_id).first()
        cost_price = prod.cost_price if prod else 250.0
        selling_price = prod.selling_price if prod else 499.0
        result = PriceOptimizationEngine.optimize_price(cost_price=cost_price, current_price=selling_price)
        if "curve_df" in result and isinstance(result["curve_df"], pd.DataFrame):
            result["pricing_curve"] = result["curve_df"].to_dict(orient="records")
            del result["curve_df"]
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message=f"Computed optimal pricing curve for product {product_id}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price optimization error: {str(e)}")
