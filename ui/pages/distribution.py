import streamlit as st

from core.services.analysis_service import analyze_distribution_input
from core.recommendations.distribution import generate_distribution_recommendations
from storage.db import save_distribution_record
from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.charts.gauge import build_risk_gauge
from ui.charts.pie import build_loss_pie_chart
from ui.charts.bar import build_load_chart


def render_distribution_page():
    render_header(
        "Distribution Analysis",
        "Analyze feeder, DT loading, consumer voltage, and distribution losses.",
    )

    with st.form("distribution_form"):
        col1, col2 = st.columns(2)

        with col1:
            zone_name = st.text_input("Zone Name", "Yangon")
            feeder_name = st.text_input("Feeder Name", "Feeder-01")
            feeder_load_mw = st.number_input("Feeder Load (MW)", value=18.0)
            dt_rating_mva = st.number_input("DT Rating (MVA)", value=25.0)

        with col2:
            dt_load_mw = st.number_input("DT Load (MW)", value=19.0)
            consumer_voltage_v = st.number_input("Consumer Voltage (V)", value=218.0)
            technical_loss_pct = st.number_input("Technical Loss (%)", value=8.0)
            non_technical_loss_pct = st.number_input("Non-Technical Loss (%)", value=4.0)

        submitted = st.form_submit_button("Analyze Distribution")

    if submitted:
        inputs = {
            "zone_name": zone_name,
            "feeder_name": feeder_name,
            "feeder_load_mw": feeder_load_mw,
            "dt_rating_mva": dt_rating_mva,
            "dt_load_mw": dt_load_mw,
            "consumer_voltage_v": consumer_voltage_v,
            "technical_loss_pct": technical_loss_pct,
            "non_technical_loss_pct": non_technical_loss_pct,
        }

        result = analyze_distribution_input(inputs)
        save_distribution_record(result)

        st.success("Distribution analysis complete and saved.")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Loss (%)", result["total_loss_pct"])
        c2.metric("DT Loading (%)", result["dt_loading_pct"])
        c3.metric("Voltage (V)", result["consumer_voltage_v"])
        c4.metric("Risk Score", result["risk_score"])

        st.markdown("---")

        left, right = st.columns(2)

        with left:
            st.plotly_chart(build_risk_gauge(result["risk_score"]), use_container_width=True)

        with right:
            render_risk_badge(result["risk_level"])
            st.write(f"**Zone:** {result['zone_name']}")
            st.write(f"**Feeder:** {result['feeder_name']}")
            st.write(f"**Created At:** {result['created_at']}")

        st.markdown("---")

        chart1, chart2 = st.columns(2)

        with chart1:
            st.plotly_chart(
                build_load_chart(result["dt_load_mw"], result["dt_rating_mva"]),
                use_container_width=True,
            )

        with chart2:
            st.plotly_chart(
                build_loss_pie_chart(result["technical_loss_pct"], result["non_technical_loss_pct"]),
                use_container_width=True,
            )

        st.markdown("### Detected Issues")
        for item in result["issues"].split("\n"):
            st.write(f"- {item}")

        st.markdown("### Recommendations")
        for rec in generate_distribution_recommendations(result):
            st.write(f"- {rec}")
