import streamlit as st
from ui.components.header import render_header
from ui.maps.myanmar_map import build_myanmar_asset_map


def render_map_page():
    render_header(
        "Myanmar Map",
        "Starter geospatial view for GT&D assets and key zones.",
    )

    st.plotly_chart(build_myanmar_asset_map(), use_container_width=True)

    st.info("This is the Phase 3 starter map. Later phases can add generation sites, substations, lines, and risk layers.")
