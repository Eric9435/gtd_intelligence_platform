import streamlit as st
from ui.components.header import render_header
from ui.maps.myanmar_map import build_myanmar_asset_map
from ui.maps.risk_map import build_myanmar_risk_map


def render_map_page():
    render_header(
        "Myanmar Map",
        "Geospatial asset and risk view using CSV-backed GT&D data.",
    )

    tab1, tab2 = st.tabs(["Asset Map", "Risk Map"])

    with tab1:
        st.plotly_chart(build_myanmar_asset_map(), use_container_width=True)

    with tab2:
        st.plotly_chart(build_myanmar_risk_map(), use_container_width=True)
