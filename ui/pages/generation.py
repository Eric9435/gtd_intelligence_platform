import streamlit as st

from core.services.analysis_service import analyze_generation_input
from core.recommendations.generation import generate_generation_recommendations
from storage.db import save_generation_record
from ui.components.header import render_header
from ui.components.kpi_cards import render_kpi_cards
from ui.components.alerts import render_risk_badge
from ui.charts.gauge import build_risk_gauge
from ui.charts.trend import build_generation_capacity_chart


def render_generation_page():
    render_header(
        "Generation Analysis",
        "Evaluate generation plant utilization, reserve margin, and performance risk.",
    )

    with st.form("generation_form"):
        col1, col2 = st.columns(2)

        with col1:
            plant_name = st.text_input("Plant Name", "Yeywa")
            plant_type = st.selectbox("Plant Type", ["Hydro", "Gas", "Solar", "Diesel"])
            installed_capacity_mw = st.number_input("Installed Capacity (MW)", value=790.0)

        with col2:
            available_capacity_mw = st.number_input("Available Capacity (MW)", value=720.0)
            actual_generation_mw = st.number_input("Actual Generation (MW)", value=640.0)
            efficiency_pct = st.number_input("Efficiency (%)", value=88.0)

        submitted = st.form_submit_button("Analyze Generation")

    if submitted:
        inputs = {
            "plant_name": plant_name,
            "plant_type": plant_type,
            "installed_capacity_mw": installed_capacity_mw,
            "available_capacity_mw": available_capacity_mw,
            "actual_generation_mw": actual_generation_mw,
            "efficiency_pct": efficiency_pct,
        }

        result = analyze_generation_input(inputs)
        save_generation_record(result)

        st.success("Generation analysis complete and saved.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Utilization (%)", result["utilization_pct"])
        col2.metric("Reserve Margin (MW)", result["reserve_margin_mw"])
        col3.metric("Efficiency (%)", result["efficiency_pct"])
        col4.metric("Risk Score", result["risk_score"])

        st.markdown("---")

        left, right = st.columns(2)

        with left:
            st.plotly_chart(build_risk_gauge(result["risk_score"]), use_container_width=True)

        with right:
            render_risk_badge(result["risk_level"])
            st.write(f"**Plant:** {result['plant_name']}")
            st.write(f"**Type:** {result['plant_type']}")
            st.write(f"**Created At:** {result['created_at']}")

        st.markdown("---")

        st.plotly_chart(
            build_generation_capacity_chart(
                result["actual_generation_mw"],
                result["available_capacity_mw"],
                result["installed_capacity_mw"],
            ),
            use_container_width=True,
        )

        st.markdown("### Detected Issues")
        for item in result["issues"].split("\n"):
            st.write(f"- {item}")

        st.markdown("### Recommendations")
        for rec in generate_generation_recommendations(result):
            st.write(f"- {rec}")
