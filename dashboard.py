import streamlit as st
import requests
import pandas as pd

# Set up clean web page metadata
st.set_page_config(page_title="EcoOps AI Dashboard", page_icon="🌱", layout="wide")

st.title("🌱 EcoOps AI - Enterprise Sustainability Portal")
st.markdown(
    "Automating clean computing and reducing enterprise Scope 3 carbon footprints."
)

st.write("---")

# Layout columns for key metrics
col1, col2, col3 = st.columns(3)

# 1. Fetch live data from our running FastAPI server paths
try:
    grid_response = requests.get("http://localhost:8000/api/v1/grid-status").json()
    ai_response = requests.get("http://localhost:8000/api/v1/ai-recommendation").json()

    current_intensity = grid_response["carbon_intensity"]
    best_hour = ai_response["recommended_hour_24h"]
    predicted_intensity = ai_response["predicted_carbon_intensity"]

    # Calculate carbon reduction savings percentage for display
    savings_pct = round(
        ((current_intensity - predicted_intensity) / current_intensity) * 100, 1
    )

    with col1:
        st.metric(
            label="Current Grid Carbon Intensity",
            value=f"{current_intensity} gCO2/kWh",
            delta="High Pollution" if current_intensity > 300 else "Stable Mix",
            delta_color="inverse",
        )

    with col2:
        st.metric(
            label="AI Recommended Run Time",
            value=f"{best_hour}:00 Local Time",
            delta="Optimal Window",
        )

    with col3:
        st.metric(
            label="Predicted Carbon Drop",
            value=f"{predicted_intensity} gCO2/kWh",
            delta=f"-{savings_pct}% Carbon Emitted",
        )

except Exception as e:
    st.error(
        "Could not connect to the EcoOps AI core server. Please verify Uvicorn is running on port 8000."
    )

st.write("---")

# Interacting and Scheduling Section
st.subheader("🤖 Automated Task Scheduler Agent")
st.write(
    "Submit non-urgent code or pipeline infrastructure to let the AI execute it at the greenest window."
)

with st.form("task_scheduler_form"):
    task_name = st.text_input(
        "Enter Cloud Job Name:", value="Daily Database Backup Pipeline"
    )
    developer_group = st.selectbox(
        "Engineering Team Cluster:",
        ["Data Science Core", "DevOps Infrastructure", "QA Automation Testing"],
    )

    submit_button = st.form_submit_button("Route Task to EcoOps Agent")

    if submit_button:
        st.success(
            f"🚀 Task '{task_name}' successfully intercepted! The AI Agent has scheduled execution for {best_hour}:00 to lower carbon footprint."
        )
