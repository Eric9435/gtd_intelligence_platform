import streamlit as st

from core.services.analysis_service import analyze_roi_input
from storage.db import save_roi_record
from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.charts.gauge import build_risk_gauge
from ui.charts.bar import build_money_bar_chart


def render_roi_page():
    render_header(
        "ROI Analysis",
        "Evaluate CAPEX, OPEX, annual revenue, annual profit, ROI, and payback.",
    )

    with st.form("roi_form"):
        col1, col2 = st.columns(2)

        with col1:
            project_name = st.text_input("Project Name", "National Upgrade Program")
            capex_mmk = st.number_input("CAPEX (MMK)", value=50000000000.0)
            opex_monthly_mmk = st.number_input("OPEX Monthly (MMK)", value=800000000.0)

        with col2:
            annual_revenue_mmk = st.number_input("Annual Revenue (MMK)", value=18000000000.0)

        submitted = st.form_submit_button("Analyze ROI")

    if submitted:
        inputs = {
            "project_name": project_name,
            "capex_mmk": capex_mmk,
            "opex_monthly_mmk": opex_monthly_mmk,
            "annual_revenue_mmk": annual_revenue_mmk,
        }

        result = analyze_roi_input(inputs)
        save_roi_record(result)

        st.success("ROI analysis complete and saved.")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Annual Profit", f"{result['annual_profit_mmk']:,.0f}")
        c2.metric("ROI (%)", result["roi_pct"])
        c3.metric("Payback (Years)", result["payback_years"])
        c4.metric("Risk Score", result["risk_score"])

        st.markdown("---")

        left, right = st.columns(2)

        with left:
            st.plotly_chart(build_risk_gauge(result["risk_score"]), use_container_width=True)

        with right:
            render_risk_badge(result["risk_level"])
            st.write(f"**Project:** {result['project_name']}")
            st.write(f"**Created At:** {result['created_at']}")

        st.markdown("---")

        st.plotly_chart(
            build_money_bar_chart(
                ["CAPEX", "Annual Revenue", "Annual Profit"],
                [result["capex_mmk"], result["annual_revenue_mmk"], result["annual_profit_mmk"]],
                "Financial Overview",
            ),
            use_container_width=True,
        )

        st.markdown("### Detected Issues")
        for item in result["issues"].split("\n"):
            st.write(f"- {item}")
