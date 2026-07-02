from datetime import datetime
import altair as alt
import classifier
import database  # Permanent storage layer
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="EcoOps AI Dashboard", page_icon="🌱", layout="wide")

st.title("🌱 EcoOps AI - Enterprise Sustainability Portal")
st.markdown(
    "Automating clean computing and reducing enterprise Scope 3 carbon footprints."
)
st.write("---")

col1, col2, col3 = st.columns(3)

# FIX: Initialize baseline fallbacks to protect form submissions from crashing with NameErrors
backend_online = False
savings_pct = 0.0
best_hour = 0

try:
    grid_response = requests.get("http://localhost:8000/api/v1/grid-status").json()
    ai_response = requests.get("http://localhost:8000/api/v1/ai-recommendation").json()

    current_intensity = grid_response["carbon_intensity"]
    best_hour = ai_response["recommended_hour_24h"]
    predicted_intensity = ai_response["predicted_carbon_intensity"]

    # Calculate actual percentage savings dynamically
    savings_pct = round(
        ((current_intensity - predicted_intensity) / current_intensity) * 100, 1
    )
    backend_online = True

    with col1:
        st.metric(
            label="Current Grid Carbon Intensity",
            value=f"{current_intensity} gCO2/kWh",
        )
    with col2:
        st.metric(label="AI Recommended Run Time", value=f"{best_hour}:00 Local Time")
    with col3:
        st.metric(
            label="Predicted Carbon Drop",
            value=f"{predicted_intensity} gCO2/kWh",
            delta=f"-{savings_pct}% Carbon",
        )

    # Render the 24-Hour Forecast Chart
    st.write("---")
    st.subheader("📊 AI-Predicted 24-Hour Regional Grid Carbon Timeline")
    forecast_data = pd.DataFrame(ai_response["hourly_forecast"])

    chart = (
        alt.Chart(forecast_data)
        .mark_line(color="#10b981", strokeWidth=3)
        .encode(
            x=alt.X(
                "hour:Q",
                title="Hour of the Day (24h Scale)",
                scale=alt.Scale(domain=[0, 23]),
            ),
            y=alt.Y("predicted_intensity:Q", title="Carbon Intensity (gCO2/kWh)"),
            tooltip=["hour", "predicted_intensity"],
        )
        .properties(height=300)
        .interactive()
    )

    points = (
        alt.Chart(forecast_data)
        .mark_point(color="#34d399", size=60)
        .encode(x="hour:Q", y="predicted_intensity:Q")
    )
    st.altair_chart(chart + points, use_container_width=True)

except Exception as e:
    st.error(
        "Could not connect to the EcoOps AI core server. Please verify Uvicorn is running on port 8000."
    )

st.write("---")

# Interacting and Scheduling Section
st.subheader("🤖 Automated Task Scheduler Agent")

with st.form("task_scheduler_form"):
    task_name = st.text_input(
        "Enter Cloud Job Name:",
        value="Run regular batch backup of historical user analytics databases",
    )
    developer_group = st.selectbox(
        "Engineering Team Cluster:",
        ["Data Science Core", "DevOps Infrastructure", "QA Automation Testing"],
    )

    submit_button = st.form_submit_button("Route Task to EcoOps Agent")

    if submit_button:
        # FIX: Explicit safeguard preventing submissions if core backend is down
        if not backend_online:
            st.error(
                "Cannot route scheduling tasks while the core optimization server is offline."
            )
        else:
            with st.spinner("🤖 AI Agent evaluating workflow safety impact..."):
                ai_decision = classifier.classify_cloud_task(task_name)
                classification = ai_decision["classification"]
                reason = ai_decision["reason"]

                # If the task is mission-critical, it runs instantly (0% carbon delay savings)
                final_savings = (
                    0.0 if classification == "Mission-Critical" else savings_pct
                )
                final_run_hour = (
                    datetime.now().hour
                    if classification == "Mission-Critical"
                    else best_hour
                )

                # Log the snapshot record safely to the database file
                database.log_task(
                    task_name,
                    developer_group,
                    classification,
                    final_run_hour,
                    final_savings,
                )

            st.write("### 📋 AI Assessment Breakdown:")
            if classification == "Delay-Tolerant":
                st.success(f"✅ **Status: {classification}**")
                st.info(
                    f"🔮 **AI Scheduling Action:** This task has been successfully delayed. It will execute later today at **{best_hour}:00** when the grid is cleanest."
                )
            else:
                st.warning(f"⚠️ **Status: {classification}**")
                st.info(
                    f"🚀 **AI Scheduling Action:** This job affects production/users. Bypassing green delays to guarantee server performance. **Executing instantly.**"
                )

            st.write(f"*AI Contextual Reasoning:* {reason}")

# DISPLAY HISTORIC AUDIT LOG TABLE
st.write("---")
st.subheader("📜 Enterprise Core Green Audit Logs")
st.markdown(
    "A permanent historical ledger of all intercepted pipelines managed by the optimization agent."
)

# Pull live logs from our database file
raw_logs = database.get_all_logs()

if raw_logs:
    # Format database rows into a clean, searchable visual data grid table
    log_df = pd.DataFrame(
        raw_logs,
        columns=[
            "Task Name",
            "Engineering Team",
            "AI Classification",
            "Scheduled Hour",
            "Carbon Saved %",
            "Logged Timestamp",
        ],
    )
    st.dataframe(log_df, use_container_width=True)
else:
    st.info(
        "No tasks logged yet. Submit your first cloud job above to generate an audit entry!"
    )
