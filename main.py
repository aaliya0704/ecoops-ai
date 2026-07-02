import os  # <-- NEW: For reading environment configurations
from datetime import datetime, timezone
import math
from typing import Dict, List

import brain
from dotenv import load_dotenv  # <-- NEW: For loading the .env file
from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel
import requests

# Load environment mappings at application startup
load_dotenv()

app = FastAPI(title="EcoOps AI - Unified Core Engine")

# Read the URL securely from the environment with a backup fallback
GRID_API_URL = os.getenv(
    "PUBLIC_GRID_API_URL", "https://api.carbonintensity.org.uk/intensity"
)


class GridMetric(BaseModel):
    region: str
    carbon_intensity: int
    timestamp: str
    source: str


class AIRecommendation(BaseModel):
    recommended_hour_24h: int
    predicted_carbon_intensity: float
    hourly_forecast: List[Dict[str, float]]
    status: str


@app.get("/")
def root():
    return {"status": "EcoOps AI Integrated Core Operational"}


@app.get("/api/v1/grid-status", response_model=GridMetric)
def get_live_grid_data(region: str = "UK-MAIN"):
    try:
        # Securely using the environment variable instead of a hardcoded string
        response = requests.get(GRID_API_URL, timeout=4)

        if response.status_code == 200:
            data = response.json()
            live_intensity = data["data"][0]["intensity"]["actual"]

            if live_intensity is None:
                live_intensity = data["data"][0]["intensity"]["forecast"]

            return {
                "region": region,
                "carbon_intensity": int(live_intensity),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "National Grid ESO Live API Gateway",
            }

    except Exception as api_error:
        print(
            f"[⚠️ Ingestion Warning] Live feed offline ({str(api_error)}). Activating smart simulation fallback..."
        )

    # ─── GRACEFUL FALLBACK SYSTEM ───
    current_hour = datetime.now().hour
    if 11 <= current_hour <= 15:
        fallback_intensity = 150
    elif 18 <= current_hour <= 22:
        fallback_intensity = 480
    else:
        fallback_intensity = 310

    return {
        "region": region,
        "carbon_intensity": fallback_intensity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "EcoOps Internal Simulation Core (API Offline Fallback)",
    }


@app.get("/api/v1/ai-recommendation", response_model=AIRecommendation)
def get_ai_scheduling_prediction(current_live_intensity: float = 310.0):
    try:
        all_hours = np.array([[h] for h in range(24)])
        predicted_scores = brain.ai_brain.predict(all_hours)

        best_hour = int(np.argmin(predicted_scores))

        model_baseline = (
            predicted_scores[datetime.now().hour]
            if datetime.now().hour < 24
            else predicted_scores[0]
        )
        scaling_ratio = current_live_intensity / model_baseline

        forecast_list = []
        for h, score in enumerate(predicted_scores):
            scaled_score = round(score * scaling_ratio, 1)
            forecast_list.append({"hour": h, "predicted_intensity": scaled_score})

        lowest_score = forecast_list[best_hour]["predicted_intensity"]

        return {
            "recommended_hour_24h": best_hour,
            "predicted_carbon_intensity": lowest_score,
            "hourly_forecast": forecast_list,
            "status": "AI Optimization Recommendation and Dynamic Forecast Synchronized Successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"AI Engine Inference Failure: {str(e)}"
        )
