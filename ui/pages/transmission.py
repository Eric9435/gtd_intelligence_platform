import streamlit as st

from core.services.analysis_service import analyze_transmission_input
from core.recommendations.transmission import generate_recommendations
from core.data_quality.validation_engine import (
    validate_positive,
    validate_power_factor,
    validate_voltage,
    build_data_quality_score,
)
from core.data_quality.anomaly_detection import detect_transmission_anomalies
from storage.db import save_transmission_record
from ui.components.header import render_header
from ui.components.kpi_cards import render_kpi_cards
from ui.components.alerts import render_risk_badge
from ui.components.data_quality_panel import render_data_quality_panel
from ui.charts.gauge import build_risk_gauge
from ui.charts.bar import build_load_chart
from ui.charts.line import build_temp_chart


def render_transmission_page():
    render_header(
        "Transmission / Substation Analysis",
        "Enter substation and transformer operating data for engineering analysis.",
    )

    with st.form("transmission_form"):
        col1, col2 = st.columns(2)

        with col1:
            substation_name = st.text_input("Substation Name", "Hlaing Tharyar")
            transformer_mva = st.number_input("Transformer Rating (MVA)", value=100.0)
            load_mw = st.number_input("Load (MW)", value=72.0)
            primary_kv = st.number_input("Primary Voltage (kV)", value=230.0)
            secondary_kv = st.number_input("Secondary Voltage (kV)", value=220.0)

        with col2:
            current_r = st.number_input("Current R (A)", value=180.0)
            current_y = st.number_input("Current Y (A)", value=175.0)
            current_b = st.number_input("Current B (A)", value=190.0)
            power_factor = st.number_input("Power Factor", value=0.90)
            oil_temp = st.number_input("Oil Temperature (°C)", value=68.0)
            winding_temp = st.number_input("Winding Temperature (°C)", value=72.0)

        submitted = st.form_submit_button("Analyze Transmission")

    if submitted:
        inputs = {
            "substation_name": substation_name,
            "transformer_mva": transformer_mva,
            "load_mw": load_mw,
            "primary_kv": primary_kv,
            "secondary_kv": secondary_kv,
            "current_r": current_r,
            "current_y": current_y,
            "current_b": current_b,
            "power_factor": power_factor,
            "oil_temp": oil_temp,
            "winding_temp": winding_temp,
        }

        quality_issues = []
        quality_issues += validate_positive("Transformer Rating", transformer_mva)
        quality_issues += validate_positive("Load", load_mw)
        quality_issues += validate_voltage("Primary Voltage", primary_kv)
        quality_issues += validate_voltage("Secondary Voltage", secondary_kv)
        quality_issues += validate_power_factor(power_factor)
        quality_issues += detect_transmission_anomalies(inputs)

        quality_score = build_data_quality_score(len(quality_issues))

        result = analyze_transmission_input(inputs)
        save_transmission_record(result)

        st.success("Analysis complete and saved.")

        render_data_quality_panel(quality_score, quality_issues)

        st.markdown("### KPI Summary")
        render_kpi_cards(result)

        st.markdown("---")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### Risk Gauge")
            st.plotly_chart(
                build_risk_gauge(result["risk_score"]),
                use_container_width=True,
            )

        with col2:
            st.markdown("### Risk Level")
            render_risk_badge(result["risk_level"])
            st.write(f"**Substation:** {result['substation_name']}")
            st.write(f"**Created At:** {result['created_at']}")
            st.write(f"**Loading:** {result['loading_pct']} %")
            st.write(f"**Average Current:** {result['avg_current']} A")

        st.markdown("---")
        st.markdown("### System Charts")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(
                build_load_chart(result["load_mw"], result["transformer_mva"]),
                use_container_width=True,
            )

        with chart_col2:
            st.plotly_chart(
                build_temp_chart(result["oil_temp"], result["winding_temp"]),
                use_container_width=True,
            )

        st.markdown("---")
        st.markdown("### Detected Issues")
        for item in result["issues"].split("\n"):
            st.write(f"- {item}")

        st.markdown("---")
        st.markdown("### Recommendations")
        recommendations = generate_recommendations(result)
        for rec in recommendations:
            st.write(f"- {rec}")
