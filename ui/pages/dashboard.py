import streamlit as st

from ui.components.header import render_header
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
)
from ui.charts.bar import build_money_bar_chart
from ui.components.alerts import render_risk_badge


def render_dashboard_page():
    render_header(
        "Integrated Dashboard",
        "Combined GT&D engineering, business, ROI, and export overview.",
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

    chart_col1, chart_col2 = st.columns(2)

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
        st.markdown("### Latest Risk Snapshot")
        st.write("**Generation Risk**")
        render_risk_badge(latest_generation.get("risk_level", "NORMAL"))
        st.write("**Transmission Risk**")
        render_risk_badge(latest_transmission.get("risk_level", "NORMAL"))
        st.write("**Distribution Risk**")
        render_risk_badge(latest_distribution.get("risk_level", "NORMAL"))
        st.write("**ROI Risk**")
        render_risk_badge(latest_roi.get("risk_level", "NORMAL"))
        st.write("**Export Risk**")
        render_risk_badge(latest_export.get("risk_level", "NORMAL"))

    st.markdown("---")

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
