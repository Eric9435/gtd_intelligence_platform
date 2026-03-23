import streamlit as st

from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.components.risk_panel import render_risk_summary_boxes
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
)


def render_executive_summary_page():
    render_header(
        "Executive Summary",
        "Official decision-ready summary for GT&D engineering, business, and risk status.",
    )

    generation = fetch_all_generation_records()
    transmission = fetch_all_transmission_records()
    distribution = fetch_all_distribution_records()
    sales = fetch_all_sales_records()
    roi = fetch_all_roi_records()
    export = fetch_all_export_records()

    latest_generation = generation[0] if generation else {}
    latest_transmission = transmission[0] if transmission else {}
    latest_distribution = distribution[0] if distribution else {}
    latest_sales = sales[0] if sales else {}
    latest_roi = roi[0] if roi else {}
    latest_export = export[0] if export else {}

    render_risk_summary_boxes([
        ("Generation", f"{latest_generation.get('actual_generation_mw', 0)} MW"),
        ("Transmission Risk", str(latest_transmission.get("risk_score", 0))),
        ("Distribution Loss", f"{latest_distribution.get('total_loss_pct', 0)} %"),
        ("Revenue", f"{latest_sales.get('revenue_mmk', 0):,.0f} MMK"),
        ("ROI", f"{latest_roi.get('roi_pct', 0)} %"),
        ("Export Revenue", f"{latest_export.get('export_revenue_mmk', 0):,.0f} MMK"),
    ])

    st.markdown("---")

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### Executive Narrative")
        st.write(
            f"""
            The latest GT&D operating profile indicates **{latest_generation.get('actual_generation_mw', 0)} MW**
            of generation, with a transmission risk score of **{latest_transmission.get('risk_score', 0)}** and
            a distribution loss level of **{latest_distribution.get('total_loss_pct', 0)} %**.
            
            Commercially, the system is currently producing **{latest_sales.get('revenue_mmk', 0):,.0f} MMK**
            in revenue, with an estimated ROI of **{latest_roi.get('roi_pct', 0)} %**.
            
            Export opportunity currently stands at **{latest_export.get('surplus_mw', 0)} MW** surplus with
            potential export revenue of **{latest_export.get('export_revenue_mmk', 0):,.0f} MMK**.
            """
        )

    with right:
        st.markdown("### Executive Risk Status")
        st.write("Generation")
        render_risk_badge(latest_generation.get("risk_level", "NORMAL"))
        st.write("Transmission")
        render_risk_badge(latest_transmission.get("risk_level", "NORMAL"))
        st.write("Distribution")
        render_risk_badge(latest_distribution.get("risk_level", "NORMAL"))
        st.write("ROI")
        render_risk_badge(latest_roi.get("risk_level", "NORMAL"))
        st.write("Export")
        render_risk_badge(latest_export.get("risk_level", "NORMAL"))
