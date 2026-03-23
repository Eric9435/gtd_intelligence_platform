import streamlit as st

from core.services.analysis_service import analyze_sales_input
from storage.db import save_sales_record
from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.charts.gauge import build_risk_gauge
from ui.charts.bar import build_money_bar_chart
from ui.charts.pie import build_loss_pie_chart


def render_sales_page():
    render_header(
        "Sales & Revenue",
        "Analyze units sold, tariff, revenue, and customer mix.",
    )

    with st.form("sales_form"):
        col1, col2 = st.columns(2)

        with col1:
            zone_name = st.text_input("Zone Name", "Yangon")
            units_sold_mwh = st.number_input("Units Sold (MWh)", value=150000.0)
            tariff_mmk_per_kwh = st.number_input("Tariff (MMK/kWh)", value=180.0)

        with col2:
            industrial_pct = st.number_input("Industrial (%)", value=45.0)
            residential_pct = st.number_input("Residential (%)", value=40.0)
            commercial_pct = st.number_input("Commercial (%)", value=15.0)

        submitted = st.form_submit_button("Analyze Sales")

    if submitted:
        inputs = {
            "zone_name": zone_name,
            "units_sold_mwh": units_sold_mwh,
            "tariff_mmk_per_kwh": tariff_mmk_per_kwh,
            "industrial_pct": industrial_pct,
            "residential_pct": residential_pct,
            "commercial_pct": commercial_pct,
        }

        result = analyze_sales_input(inputs)
        save_sales_record(result)

        st.success("Sales analysis complete and saved.")

        c1, c2, c3 = st.columns(3)
        c1.metric("Units Sold (MWh)", result["units_sold_mwh"])
        c2.metric("Tariff (MMK/kWh)", result["tariff_mmk_per_kwh"])
        c3.metric("Revenue (MMK)", f"{result['revenue_mmk']:,.0f}")

        st.markdown("---")

        left, right = st.columns(2)

        with left:
            st.plotly_chart(build_risk_gauge(result["risk_score"]), use_container_width=True)

        with right:
            render_risk_badge(result["risk_level"])
            st.write(f"**Zone:** {result['zone_name']}")
            st.write(f"**Created At:** {result['created_at']}")

        st.markdown("---")

        chart1, chart2 = st.columns(2)

        with chart1:
            st.plotly_chart(
                build_money_bar_chart(
                    ["Revenue"],
                    [result["revenue_mmk"]],
                    "Revenue Overview",
                ),
                use_container_width=True,
            )

        with chart2:
            st.plotly_chart(
                build_loss_pie_chart(
                    result["industrial_pct"],
                    result["residential_pct"] + result["commercial_pct"],
                ),
                use_container_width=True,
            )

        st.markdown("### Detected Issues")
        for item in result["issues"].split("\n"):
            st.write(f"- {item}")
