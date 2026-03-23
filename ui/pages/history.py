import streamlit as st
import pandas as pd

from ui.components.header import render_header
from storage.db import (
    fetch_all_transmission_records,
    fetch_all_generation_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
)


def render_history_page():
    render_header(
        "History",
        "Saved records for transmission, generation, distribution, sales, ROI, and export.",
    )

    tabs = st.tabs([
        "Transmission",
        "Generation",
        "Distribution",
        "Sales",
        "ROI",
        "Export",
    ])

    with tabs[0]:
        rows = fetch_all_transmission_records()
        st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No transmission records found.")

    with tabs[1]:
        rows = fetch_all_generation_records()
        st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No generation records found.")

    with tabs[2]:
        rows = fetch_all_distribution_records()
        st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No distribution records found.")

    with tabs[3]:
        rows = fetch_all_sales_records()
        st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No sales records found.")

    with tabs[4]:
        rows = fetch_all_roi_records()
        st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No ROI records found.")

    with tabs[5]:
        rows = fetch_all_export_records()
        st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No export records found.")
