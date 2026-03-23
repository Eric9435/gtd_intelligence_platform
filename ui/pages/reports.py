import streamlit as st
import pandas as pd

from ui.components.header import render_header
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
    fetch_all_sales_records,
    fetch_all_roi_records,
    fetch_all_export_records,
)
from reports.csv import export_dataframe_to_csv
from reports.pdf import build_simple_pdf_report


def render_reports_page():
    render_header(
        "Reports",
        "Export GT&D records in CSV and advanced PDF format.",
    )

    module = st.selectbox(
        "Select Module",
        ["Generation", "Transmission", "Distribution", "Sales", "ROI", "Export"],
    )

    if module == "Generation":
        rows = fetch_all_generation_records()
    elif module == "Transmission":
        rows = fetch_all_transmission_records()
    elif module == "Distribution":
        rows = fetch_all_distribution_records()
    elif module == "Sales":
        rows = fetch_all_sales_records()
    elif module == "ROI":
        rows = fetch_all_roi_records()
    else:
        rows = fetch_all_export_records()

    if not rows:
        st.info("No records available for this module.")
        return

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    csv_bytes = export_dataframe_to_csv(df)
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name=f"{module.lower()}_records.csv",
        mime="text/csv",
    )

    latest = rows[0]
    sections = {
        "Module Summary": [
            f"Module: {module}",
            f"Record Count: {len(rows)}",
        ],
        "Latest Record": [f"{k}: {v}" for k, v in latest.items()],
    }

    pdf_bytes = build_simple_pdf_report(
        title=f"{module} GT&D Report",
        sections=sections,
    )

    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=f"{module.lower()}_report.pdf",
        mime="application/pdf",
    )
