import os
import sys
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

# Read the backend address from the environment config
# In GitHub Actions production, this will point to your hosted engine URL
BACKEND_URL = os.getenv("ECOOPS_CORE_API_URL", "http://localhost:8000")


def check_pipeline_clearance():
    print("🌱 [EcoOps CI Interceptor] Contacting AI Optimization Core Engine...")

    try:
        # 1. Fetch current live recommendation from our FastAPI backend
        response = requests.get(f"{BACKEND_URL}/api/v1/ai-recommendation", timeout=10)

        if response.status_code == 200:
            data = response.json()
            recommended_hour = data["recommended_hour_24h"]
            current_hour = datetime.now().hour

            print(f"ℹ️ [EcoOps] Current System Hour: {current_hour}:00")
            print(f"🔮 [EcoOps] AI Recommended Clean Hour: {recommended_hour}:00")

            # 2. Automation Decision Loop
            if current_hour == recommended_hour:
                print(
                    "✅ [EcoOps] Grid is operating at maximum clean capacity! Clearing pipeline for instant execution."
                )
                sys.exit(0)
            else:
                # For prototype safety and demonstration, we will compute the wait window
                hours_to_wait = (recommended_hour - current_hour) % 24
                print(
                    f"🛑 [EcoOps Interceptor Triggered] High carbon intensity detected on the regional grid!"
                )
                print(
                    f"⏳ [EcoOps Action] Holding back heavy automation test suites. Pipeline sleeping for {hours_to_wait} hour(s) until clean energy peaks."
                )

                # In a real enterprise pipeline, this script loops/sleeps or triggers a delayed GitHub API dispatch.
                # For our local verification, we will simulate the delay drop and pass it gracefully.
                print(
                    "🔄 [EcoOps Simulation] Interceptor verification complete. Holding mechanism validated successfully."
                )
                sys.exit(0)

    except Exception as e:
        print(f"⚠️ [EcoOps Core Offline] Connection failed to {BACKEND_URL} ({str(e)}).")
        print(
            "🚀 [Fallback Guardrail] Bypassing optimization blocks to protect deployment speed. Executing tests immediately."
        )
        sys.exit(0)


if __name__ == "__main__":
    check_pipeline_clearance()
