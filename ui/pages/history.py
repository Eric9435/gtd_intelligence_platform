import streamlit as st
import pandas as pd

from ui.components.header import render_header
from storage.db import (
    fetch_all_transmission_records,
    fetch_all_generation_records,
    fetch_all_distribution_records,
)


def render_history_page():
    render_header(
        "History",
        "Saved transmission, generation, and distribution records.",
    )

    tab1, tab2, tab3 = st.tabs(["Transmission", "Generation", "Distribution"])

    with tab1:
        rows = fetch_all_transmission_records()
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.info("No transmission records found.")

    with tab2:
        rows = fetch_all_generation_records()
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.info("No generation records found.")

    with tab3:
        rows = fetch_all_distribution_records()
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.info("No distribution records found.")
