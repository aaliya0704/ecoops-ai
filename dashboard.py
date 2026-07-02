import os  # <-- NEW: For reading environment configurations
from datetime import datetime

import altair as alt
import classifier
import database  # Permanent storage layer
from dotenv import load_dotenv  # <-- NEW: For loading the .env file
import pandas as pd
import requests
import streamlit as st

# Load environment variables
load_dotenv()

# Read backend URL securely from environment
BACKEND_URL = os.getenv("ECOOPS_CORE_API_URL", "http://localhost:8000")

st.set_page_config(page_title="EcoOps AI Dashboard", page_icon="🌱", layout="wide")

st.title("🌱 EcoOps AI - Enterprise Sustainability Portal")
st.markdown(
    "Automating clean computing and reducing enterprise Scope 3 carbon footprints."
)
st.write("---")

col1, col2, col3 = st.columns(3)

backend_online = False
savings_pct = 0.0
best_hour = 0

try:
    # 1. Fetch current live telemetry using secure environment routing
    grid_response = requests.get(f"{BACKEND_URL}/api/v1/grid-status").json()
    current_intensity = grid_response["carbon_intensity"]

    # 2. Pass the real-world intensity directly using environment routing
    ai_response = requests.get(
        f"{BACKEND_URL}/api/v1/ai-recommendation?current_live_intensity={current_intensity}"
    ).json()

    best_hour = ai_response["recommended_hour_24h"]
    predicted_intensity = ai_response["predicted_carbon_intensity"]

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
        f"Could not connect to the EcoOps AI core server at {BACKEND_URL}. Please verify Uvicorn is running."
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
        if not backend_online:
            st.error(
                "Cannot route scheduling tasks while the core optimization server is offline."
            )
        else:
            with st.spinner("🤖 AI Agent evaluating workflow safety impact..."):
                ai_decision = classifier.classify_cloud_task(task_name)
                classification = ai_decision["classification"]
                reason = ai_decision["reason"]

                final_savings = (
                    0.0 if classification == "Mission-Critical" else savings_pct
                )
                final_run_hour = (
                    datetime.now().hour
                    if classification == "Mission-Critical"
                    else best_hour
                )

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

    # ─── FEATURE F: EXECUTIVE ANALYTICS SUMMARY SCREEN ───
    st.write("---")
    st.subheader("📊 Executive Carbon & Financial Compliance Summary (30-Day View)")
    st.markdown(
        "Cumulative multi-tenant infrastructure metrics translating grid deferrals into corporate ESG capital values."
    )

    # Mathematical conversion metrics for enterprise computing scaling
    # Assuming a standard cloud batch baseline of 0.45 Tons of CO2 per continuous cluster run
    # Assuming an average standard infrastructure server run costs $12.50 in compute hour billing
    total_delayed_tasks = len(log_df[log_df["AI Classification"] == "Delay-Tolerant"])

    total_co2_offset = round(total_delayed_tasks * 0.45, 2)
    total_usd_saved = round(total_delayed_tasks * 12.50, 2)

    # Render Executive Financial & ESG KPI Cards
    exec_col1, exec_col2, exec_col3 = st.columns(3)
    with exec_col1:
        st.metric(
            label="Total Carbon Offset (Tons)",
            value=f"{total_co2_offset} MT CO2e",
            help="Metric Tons of Carbon Dioxide equivalent diverted from regional power plants via AI-driven diurnal load shifting.",
        )
    with exec_col2:
        st.metric(
            label="Infrastructure Spend Saved",
            value=f"${total_usd_saved} USD",
            help="Total compute spend saved by deferring workloads to non-peak pricing hours and clean windows.",
        )
    with exec_col3:
        st.metric(
            label="Total Intercepted Pipelines",
            value=f"{len(log_df)} Total Runs",
            help="Total automated software compilation and data engineering tasks parsed by the EcoOps AI Core Gate.",
        )

    st.markdown("### 📋 Downloadable Compliance Documentation")

    # Convert dataframe into standard download-ready CSV payload bytes
    csv_data = log_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Export Official Corporate Compliance Report (CSV)",
        data=csv_data,
        file_name=f"ecoops_sustainability_compliance_report_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.write("### 🗂️ Detailed Pipeline Audit Trail")
    st.dataframe(log_df, use_container_width=True)

else:
    st.info(
        "No tasks logged yet. Submit your first cloud job above to generate an audit entry!"
    )
