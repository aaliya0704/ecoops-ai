import streamlit as st
import requests
import pandas as pd
import altair as alt

import classifier

st.set_page_config(page_title="EcoOps AI Dashboard", page_icon="🌱", layout="wide")

st.title("🌱 EcoOps AI - Enterprise Sustainability Portal")
st.markdown(
    "Automating clean computing and reducing enterprise Scope 3 carbon footprints."
)
st.write("---")

col1, col2, col3 = st.columns(3)

try:
    grid_response = requests.get("http://localhost:8000/api/v1/grid-status").json()
    ai_response = requests.get("http://localhost:8000/api/v1/ai-recommendation").json()

    current_intensity = grid_response["carbon_intensity"]
    best_hour = ai_response["recommended_hour_24h"]
    predicted_intensity = ai_response["predicted_carbon_intensity"]
    savings_pct = round(
        ((current_intensity - predicted_intensity) / current_intensity) * 100, 1
    )

    with col1:
        st.metric(
            label="Current Grid Carbon Intensity", value=f"{current_intensity} gCO2/kWh"
        )
    with col2:
        st.metric(label="AI Recommended Run Time", value=f"{best_hour}:00 Local Time")
    with col3:
        st.metric(
            label="Predicted Carbon Drop",
            value=f"{predicted_intensity} gCO2/kWh",
            delta=f"-{savings_pct}% Carbon",
        )

    # ──── NEW FEATURE A: RENDERING THE 24-HOUR FORECAST CHART ────
    st.write("---")
    st.subheader("📊 AI-Predicted 24-Hour Regional Grid Carbon Timeline")
    st.markdown(
        "The line visualization maps out upcoming carbon variations. Aim to execute massive processing loads in the green valleys."
    )

    # Extract the forecast array and wrap it into a pandas DataFrame
    forecast_data = pd.DataFrame(ai_response["hourly_forecast"])

    # Configure an elegant Altair line chart with point highlights
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
        .properties(height=350)
        .interactive()
    )  # Allows the chart to zoom and pan smoothly

    # Draw points on top of the line for crisp scannability
    points = (
        alt.Chart(forecast_data)
        .mark_point(color="#34d399", size=60)
        .encode(x="hour:Q", y="predicted_intensity:Q")
    )

    # Render the combined layered chart on the dashboard layout screen
    st.altair_chart(chart + points, use_container_width=True)

except Exception as e:
    st.error(
        "Could not connect to the EcoOps AI core server. Please verify Uvicorn is running on port 8000."
    )

st.write("---")

st.subheader("🤖 Automated Task Scheduler Agent")
st.write(
    "Submit non-urgent code or pipeline infrastructure to let the AI execute it at the greenest window."
)

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
        with st.spinner("🤖 AI Agent evaluating workflow safety impact..."):
            ai_decision = classifier.classify_cloud_task(task_name)
            classification = ai_decision["classification"]
            reason = ai_decision["reason"]

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
