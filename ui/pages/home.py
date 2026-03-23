import streamlit as st
from ui.components.header import render_header


def render_home_page():
    render_header(
        "GT&D Intelligence Platform",
        "Phase 7 expanded platform with data quality, compare, filters, and executive summary.",
    )

    st.markdown("### Platform Scope")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Engineering</div>
                <div class="kpi-label">Generation, transmission, distribution analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Business</div>
                <div class="kpi-label">Revenue, ROI, surplus, export analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Planning</div>
                <div class="kpi-label">Forecast and scenario evaluation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Governance</div>
                <div class="kpi-label">Data quality, compare, executive summary</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
