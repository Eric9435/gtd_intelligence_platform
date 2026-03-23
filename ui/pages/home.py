import streamlit as st
from ui.components.header import render_header


def render_home_page():
    render_header(
        "GT&D Intelligence Platform",
        "Phase 5 expanded platform with forecast, scenarios, PDF reports, and smarter dashboard.",
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
                <div class="kpi-value">Forecast</div>
                <div class="kpi-label">Demand and generation forecasting</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Scenario</div>
                <div class="kpi-label">What-if simulation and planning view</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
