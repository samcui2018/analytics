from fastapi import APIRouter
from pydantic import BaseModel
from src.app.pipelines.detectAnomaly import detect_anomalies

router = APIRouter()

# Example request model
class ForecastRequest(BaseModel):
    product_id: int
    months: int


# GET endpoint
@router.get("/health")
def health_check():
    return {"status": "API running"}

@router.get("/DetectAnomaly")
def detect_anomaly_api():

    df, graph_base64 = detect_anomalies()

    # Convert dataframe to JSON-friendly format
    result = df.to_dict(orient="records")

    return {
        "rows": len(result),
        "data": result,
        "graph": graph_base64
    }

# GET example
@router.get("/sales/{product_id}")
def get_sales(product_id: int):
    # Normally you would call a service or DB layer
    return {
        "product_id": product_id,
        "sales": [100, 120, 130, 150]
    }


# POST example
@router.post("/forecast")
def run_forecast(request: ForecastRequest):

    # Normally this would call your analytics pipeline
    # Example: pipeline.run_forecast(request.product_id)

    forecast_result = {
        "product_id": request.product_id,
        "forecast": [160, 170, 180],
        "months": request.months
    }

    return forecast_result