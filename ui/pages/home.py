import streamlit as st
from ui.components.header import render_header


def render_home_page():
    render_header(
        "GT&D Intelligence Platform",
        "Phase 3 expanded platform with transmission, generation, distribution, history, and Myanmar map.",
    )

    st.markdown("### Platform Modules")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Generation</div>
                <div class="kpi-label">Capacity, utilization, reserve margin, risk</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Transmission</div>
                <div class="kpi-label">Substation loading, voltage, thermal, imbalance</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Distribution</div>
                <div class="kpi-label">Feeder, DT loading, voltage, losses</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-value">Myanmar Map</div>
                <div class="kpi-label">Starter geospatial asset and zone view</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
