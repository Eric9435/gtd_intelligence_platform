import streamlit as st
import pandas as pd

from ui.components.header import render_header
from auth.permissions import require_admin_access
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
    fetch_all_compare_snapshots,
)


def render_admin_page():
    require_admin_access()

    render_header(
        "Admin Page",
        "Administrative visibility into saved system records and compare snapshots.",
    )

    st.markdown("### Current Session")
    st.write(f"**User:** {st.session_state.get('display_name', '-')}")
    st.write(f"**Username:** {st.session_state.get('username', '-')}")
    st.write(f"**Role:** {st.session_state.get('role', '-')}")

    tabs = st.tabs([
        "Generation",
        "Transmission",
        "Distribution",
        "Sales",
        "ROI",
        "Export",
        "Compare Snapshots",
    ])

    datasets = [
        fetch_all_generation_records(),
        fetch_all_transmission_records(),
        fetch_all_distribution_records(),
        fetch_all_sales_records(),
        fetch_all_roi_records(),
        fetch_all_export_records(),
        fetch_all_compare_snapshots(),
    ]

    names = [
        "No generation records.",
        "No transmission records.",
        "No distribution records.",
        "No sales records.",
        "No ROI records.",
        "No export records.",
        "No compare snapshots.",
    ]

    for tab, rows, empty_msg in zip(tabs, datasets, names):
        with tab:
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True)
            else:
                st.info(empty_msg)
