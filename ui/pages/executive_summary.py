import streamlit as st

from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.components.risk_panel import render_risk_summary_boxes
from ui.components.recommendation_panel import render_recommendation_panel
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
)
from core.services.summary_service import (
    generate_executive_insight,
    generate_auto_summary_paragraph,
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

    snapshot = {
        "generation": latest_generation,
        "transmission": latest_transmission,
        "distribution": latest_distribution,
        "sales": latest_sales,
        "roi": latest_roi,
        "export": latest_export,
    }

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
        st.write(generate_auto_summary_paragraph(snapshot))

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

    st.markdown("---")

    render_recommendation_panel(
        "Executive Smart Summary",
        generate_executive_insight(snapshot),
    )
