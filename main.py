from datetime import (
    datetime,
    timezone,
)  # FIX: Added timezone to fix the utcnow deprecation
from typing import Dict, List
import brain
from fastapi import FastAPI, HTTPException
import numpy as np  # FIX: Lifted import up to the global scope
from pydantic import BaseModel

app = FastAPI(title="EcoOps AI - Unified Core Engine")


class GridMetric(BaseModel):
    region: str
    carbon_intensity: int
    timestamp: str
    source: str


class AIRecommendation(BaseModel):
    recommended_hour_24h: int
    predicted_carbon_intensity: float
    hourly_forecast: List[Dict[str, float]]  # Returns the full 24h array
    status: str


@app.get("/")
def root():
    return {"status": "EcoOps AI Integrated Core Operational"}


@app.get("/api/v1/grid-status", response_model=GridMetric)
def get_live_grid_data(region: str = "US-NW"):
    current_hour = datetime.now().hour
    if 11 <= current_hour <= 15:
        mock_intensity = 150
    elif 18 <= current_hour <= 22:
        mock_intensity = 480
    else:
        mock_intensity = 310

    return {
        "region": region,
        "carbon_intensity": mock_intensity,
        # FIX: Swapped out deprecated utcnow() for modern timezone-aware syntax
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "ElectricityMaps V3 API Gateway",
    }


@app.get("/api/v1/ai-recommendation", response_model=AIRecommendation)
def get_ai_scheduling_prediction():
    try:
        # Get the best hour and the raw predictions array from brain.py
        all_hours = np.array([[h] for h in range(24)])
        predicted_scores = brain.ai_brain.predict(all_hours)

        best_hour = int(np.argmin(predicted_scores))
        lowest_score = round(predicted_scores[best_hour], 1)

        # Format the 24-hour prediction array as a list of dictionaries for JSON compatibility
        forecast_list = [
            {"hour": h, "predicted_intensity": round(score, 1)}
            for h, score in enumerate(predicted_scores)
        ]

        return {
            "recommended_hour_24h": best_hour,
            "predicted_carbon_intensity": lowest_score,
            "hourly_forecast": forecast_list,
            "status": "AI Optimization Recommendation and Forecast Generated Successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"AI Engine Inference Failure: {str(e)}"
        )
