import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime


def train_carbon_predictor():
    """
    Simulates a historical dataset of power grid behavior and
    trains a Machine Learning model to forecast cleaner windows.
    """
    # 1. Create a historical dataset (Simulating 30 days of hourly grid data)
    np.random.seed(42)
    hours = np.tile(np.arange(24), 30)  # 0 to 23 repeated 30 times

    # Real-world logic: Carbon is higher in evening (coal/gas) and lower at noon (solar)
    base_carbon = []
    for h in hours:
        if 11 <= h <= 15:
            base_carbon.append(150 + np.random.randint(-20, 20))  # Green window
        elif 18 <= h <= 22:
            base_carbon.append(480 + np.random.randint(-40, 40))  # Dirty window
        else:
            base_carbon.append(310 + np.random.randint(-30, 30))  # Baseline Mix

    # Structure the data into a Data Table (DataFrame)
    dataset = pd.DataFrame({"hour_of_day": hours, "carbon_intensity": base_carbon})

    # 2. Separate into Features (X) and Target (y)
    X = dataset[["hour_of_day"]]  # What the AI learns from
    y = dataset["carbon_intensity"]  # What the AI is trying to predict

    # 3. Initialize and train a Random Forest Regressor Model
    # This is an ensemble model that creates decision trees to learn patterns.
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    print("🤖 EcoOps AI Engine: Training Machine Learning Model...")
    model.fit(X, y)
    print("✅ Training Complete! Model optimized successfully.")

    return model


# Initialize the global trained model instance
ai_brain = train_carbon_predictor()


def get_cleanest_scheduling_window():
    """
    Uses the trained AI to evaluate all 24 hours of the day
    and returns the best time to run heavy code tasks.
    """
    all_hours = np.array([[h] for h in range(24)])

    # AI predicts the carbon score for every single upcoming hour
    predicted_scores = ai_brain.predict(all_hours)

    # Find the hour that returned the lowest predicted carbon footprint
    best_hour = int(np.argmin(predicted_scores))
    lowest_score = round(predicted_scores[best_hour], 1)

    return {
        "recommended_hour_24h": best_hour,
        "predicted_carbon_intensity": lowest_score,
    }


# Quick test verification when running file directly
if __name__ == "__main__":
    result = get_cleanest_scheduling_window()
    print(
        f"\n[TEST RESULT] AI Recommendation: Schedule heavy tasks at {result['recommended_hour_24h']}:00"
    )
    print(
        f"[TEST RESULT] Expected Carbon Intensity: {result['predicted_carbon_intensity']} gCO2/kWh"
    )
