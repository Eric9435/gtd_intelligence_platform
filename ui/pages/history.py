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


def _filter_dataframe(df: pd.DataFrame, keyword: str):
    if not keyword:
        return df
    keyword = keyword.lower()
    mask = df.astype(str).apply(lambda col: col.str.lower().str.contains(keyword, na=False))
    return df[mask.any(axis=1)]


def render_history_page():
    render_header(
        "History",
        "Saved records with smart filtering for engineering and business review.",
    )

    keyword = st.text_input("Search keyword", "")

    tabs = st.tabs([
        "Transmission",
        "Generation",
        "Distribution",
        "Sales",
        "ROI",
        "Export",
    ])

    datasets = [
        fetch_all_transmission_records(),
        fetch_all_generation_records(),
        fetch_all_distribution_records(),
        fetch_all_sales_records(),
        fetch_all_roi_records(),
        fetch_all_export_records(),
    ]

    empty_msgs = [
        "No transmission records found.",
        "No generation records found.",
        "No distribution records found.",
        "No sales records found.",
        "No ROI records found.",
        "No export records found.",
    ]

    for tab, rows, empty_msg in zip(tabs, datasets, empty_msgs):
        with tab:
            if rows:
                df = pd.DataFrame(rows)
                df = _filter_dataframe(df, keyword)
                st.dataframe(df, use_container_width=True)
            else:
                st.info(empty_msg)
