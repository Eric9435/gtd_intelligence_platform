import streamlit as st

from core.services.analysis_service import analyze_export_input
from storage.db import save_export_record
from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.charts.gauge import build_risk_gauge
from ui.charts.bar import build_money_bar_chart
from ui.charts.line import build_export_line_chart


def render_export_page():
    render_header(
        "Surplus / Export Analysis",
        "Calculate surplus generation, export energy, and export revenue potential.",
    )

    with st.form("export_form"):
        col1, col2 = st.columns(2)

        with col1:
            zone_name = st.text_input("Zone Name", "Myanmar Grid")
            total_generation_mw = st.number_input("Total Generation (MW)", value=4200.0)
            total_demand_mw = st.number_input("Total Demand (MW)", value=3600.0)

        with col2:
            export_hours = st.number_input("Export Hours", value=8.0)
            export_tariff_mmk_per_kwh = st.number_input("Export Tariff (MMK/kWh)", value=220.0)

        submitted = st.form_submit_button("Analyze Export")

    if submitted:
        inputs = {
            "zone_name": zone_name,
            "total_generation_mw": total_generation_mw,
            "total_demand_mw": total_demand_mw,
            "export_hours": export_hours,
            "export_tariff_mmk_per_kwh": export_tariff_mmk_per_kwh,
        }

        result = analyze_export_input(inputs)
        save_export_record(result)

        st.success("Export analysis complete and saved.")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Surplus (MW)", result["surplus_mw"])
        c2.metric("Export Energy (MWh)", result["export_energy_mwh"])
        c3.metric("Export Revenue (MMK)", f"{result['export_revenue_mmk']:,.0f}")
        c4.metric("Risk Score", result["risk_score"])

        st.markdown("---")

        left, right = st.columns(2)

        with left:
            st.plotly_chart(build_risk_gauge(result["risk_score"]), use_container_width=True)

        with right:
            render_risk_badge(result["risk_level"])
            st.write(f"**Zone:** {result['zone_name']}")
            st.write(f"**Created At:** {result['created_at']}")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                build_money_bar_chart(
                    ["Generation", "Demand", "Surplus"],
                    [
                        result["total_generation_mw"],
                        result["total_demand_mw"],
                        result["surplus_mw"],
                    ],
                    "Generation vs Demand vs Surplus",
                ),
                use_container_width=True,
            )

        with col2:
            st.plotly_chart(
                build_export_line_chart(
                    ["Surplus MW", "Export MWh", "Export Revenue"],
                    [
                        result["surplus_mw"],
                        result["export_energy_mwh"],
                        result["export_revenue_mmk"],
                    ],
                    "Export Profile",
                ),
                use_container_width=True,
            )

        st.markdown("### Detected Issues")
        for item in result["issues"].split("\n"):
            st.write(f"- {item}")
