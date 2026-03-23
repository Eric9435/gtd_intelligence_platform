import streamlit as st

from ui.components.header import render_header
from ui.components.alerts import render_risk_badge
from ui.components.risk_panel import render_risk_summary_boxes
from ui.components.recommendation_panel import render_recommendation_panel
from ui.components.animations import render_animated_status_box
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
)
from ui.charts.bar import build_money_bar_chart
from core.recommendations.business import generate_business_recommendations
from core.recommendations.priority import classify_priority, build_priority_message


def render_dashboard_page():
    render_header(
        "Integrated Dashboard",
        "Combined GT&D engineering, business, planning, and risk intelligence.",
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

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Generation (MW)", latest_generation.get("actual_generation_mw", 0))
    c2.metric("Transmission Risk", latest_transmission.get("risk_score", 0))
    c3.metric("Distribution Loss (%)", latest_distribution.get("total_loss_pct", 0))
    c4.metric("Revenue (MMK)", f"{latest_sales.get('revenue_mmk', 0):,.0f}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("ROI (%)", latest_roi.get("roi_pct", 0))
    c6.metric("Annual Profit", f"{latest_roi.get('annual_profit_mmk', 0):,.0f}")
    c7.metric("Export Revenue", f"{latest_export.get('export_revenue_mmk', 0):,.0f}")
    c8.metric("Surplus (MW)", latest_export.get("surplus_mw", 0))

    st.markdown("---")

    render_risk_summary_boxes([
        ("Generation Risk", latest_generation.get("risk_level", "NORMAL")),
        ("Transmission Risk", latest_transmission.get("risk_level", "NORMAL")),
        ("Distribution Risk", latest_distribution.get("risk_level", "NORMAL")),
        ("Business Priority", classify_priority(float(latest_roi.get("risk_score", 0)))),
        ("Export Status", latest_export.get("risk_level", "NORMAL")),
        ("Action", build_priority_message(float(latest_transmission.get("risk_score", 0)))),
    ])

    st.markdown("---")

    chart_col1, chart_col2 = st.columns([1.3, 1])

    with chart_col1:
        st.plotly_chart(
            build_money_bar_chart(
                ["Generation", "Revenue", "Profit", "Export Revenue"],
                [
                    latest_generation.get("actual_generation_mw", 0),
                    latest_sales.get("revenue_mmk", 0),
                    latest_roi.get("annual_profit_mmk", 0),
                    latest_export.get("export_revenue_mmk", 0),
                ],
                "Integrated Business + Engineering Overview",
            ),
            use_container_width=True,
        )

    with chart_col2:
        st.markdown("### Risk Snapshot")
        st.write("**Generation**")
        render_risk_badge(latest_generation.get("risk_level", "NORMAL"))
        st.write("**Transmission**")
        render_risk_badge(latest_transmission.get("risk_level", "NORMAL"))
        st.write("**Distribution**")
        render_risk_badge(latest_distribution.get("risk_level", "NORMAL"))
        st.write("**ROI**")
        render_risk_badge(latest_roi.get("risk_level", "NORMAL"))
        st.write("**Export**")
        render_risk_badge(latest_export.get("risk_level", "NORMAL"))

    st.markdown("---")

    a1, a2, a3 = st.columns(3)
    with a1:
        render_animated_status_box("Grid Status", latest_export.get("risk_level", "NORMAL"), latest_export.get("risk_level", "NORMAL"))
    with a2:
        render_animated_status_box("Finance Status", latest_roi.get("risk_level", "NORMAL"), latest_roi.get("risk_level", "NORMAL"))
    with a3:
        render_animated_status_box("Transmission Status", latest_transmission.get("risk_level", "NORMAL"), latest_transmission.get("risk_level", "NORMAL"))

    st.markdown("---")

    business_context = {
        "revenue_mmk": latest_sales.get("revenue_mmk", 0),
        "roi_pct": latest_roi.get("roi_pct", 0),
        "surplus_mw": latest_export.get("surplus_mw", 0),
        "export_revenue_mmk": latest_export.get("export_revenue_mmk", 0),
        "annual_profit_mmk": latest_roi.get("annual_profit_mmk", 0),
        "payback_years": latest_roi.get("payback_years", 0),
    }
    render_recommendation_panel(
        "AI-Style Business Recommendations",
        generate_business_recommendations(business_context),
    )

    st.markdown("### Latest Snapshot (JSON)")
    snapshot = {
        "generation": latest_generation,
        "transmission": latest_transmission,
        "distribution": latest_distribution,
        "sales": latest_sales,
        "roi": latest_roi,
        "export": latest_export,
    }
    st.json(snapshot)
