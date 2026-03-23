import streamlit as st

from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from core.scenarios.what_if import run_what_if_scenario
from ui.charts.bar import build_money_bar_chart


def render_scenario_page():
    render_header(
        "What-If Scenario Analysis",
        "Test demand increase, generation drop, and system loss scenarios.",
    )

    col1, col2 = st.columns(2)

    with col1:
        base_generation_mw = st.number_input("Base Generation (MW)", value=4200.0)
        generation_change_pct = st.number_input("Generation Change (%)", value=-5.0)

    with col2:
        base_demand_mw = st.number_input("Base Demand (MW)", value=3600.0)
        demand_change_pct = st.number_input("Demand Change (%)", value=8.0)

    loss_pct = st.number_input("System Loss (%)", value=12.0)

    if st.button("Run Scenario"):
        result = run_what_if_scenario(
            base_generation_mw=base_generation_mw,
            base_demand_mw=base_demand_mw,
            generation_change_pct=generation_change_pct,
            demand_change_pct=demand_change_pct,
            loss_pct=loss_pct,
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("New Generation", result["new_generation_mw"])
        c2.metric("Available After Loss", result["available_after_loss_mw"])
        c3.metric("New Demand", result["new_demand_mw"])
        c4.metric("Surplus / Deficit", result["surplus_deficit_mw"])

        st.markdown("### Scenario Status")
        render_risk_badge(result["risk_level"])
        st.write(f"**Status:** {result['status']}")

        st.plotly_chart(
            build_money_bar_chart(
                ["Generation", "Available After Loss", "Demand", "Surplus/Deficit"],
                [
                    result["new_generation_mw"],
                    result["available_after_loss_mw"],
                    result["new_demand_mw"],
                    result["surplus_deficit_mw"],
                ],
                "Scenario Balance",
            ),
            use_container_width=True,
        )

        st.json(result)
