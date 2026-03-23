import streamlit as st
import pandas as pd

from ui.components.header import render_header
from storage.db import (
    fetch_all_generation_records,
    fetch_all_transmission_records,
    fetch_all_distribution_records,
)
from ui.charts.bar import build_money_bar_chart


def _safe_get(df: pd.DataFrame, col: str, idx: int):
    try:
        return df.iloc[idx][col]
    except Exception:
        return 0


def render_compare_page():
    render_header(
        "Compare",
        "Compare saved records side by side for engineering review.",
    )

    module = st.selectbox(
        "Select Compare Module",
        ["Transmission", "Generation", "Distribution"],
    )

    if module == "Transmission":
        rows = fetch_all_transmission_records()
        key_metrics = ["loading_pct", "risk_score", "avg_current", "imbalance_pct", "voltage_dev_pct"]
    elif module == "Generation":
        rows = fetch_all_generation_records()
        key_metrics = ["actual_generation_mw", "utilization_pct", "reserve_margin_mw", "efficiency_pct", "risk_score"]
    else:
        rows = fetch_all_distribution_records()
        key_metrics = ["feeder_load_mw", "dt_loading_pct", "consumer_voltage_v", "total_loss_pct", "risk_score"]

    if len(rows) < 2:
        st.info("At least two saved records are needed for comparison.")
        return

    df = pd.DataFrame(rows)

    idx1 = st.selectbox("Record A", options=df.index.tolist(), format_func=lambda x: f"#{df.iloc[x]['id']} - {df.iloc[x]['created_at']}")
    idx2 = st.selectbox("Record B", options=df.index.tolist(), index=1, format_func=lambda x: f"#{df.iloc[x]['id']} - {df.iloc[x]['created_at']}")

    rec1 = df.iloc[idx1].to_dict()
    rec2 = df.iloc[idx2].to_dict()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Record A")
        st.json(rec1)

    with c2:
        st.markdown("### Record B")
        st.json(rec2)

    labels = []
    values_a = []
    values_b = []

    for metric in key_metrics:
        labels.append(metric)
        values_a.append(_safe_get(df, metric, idx1))
        values_b.append(_safe_get(df, metric, idx2))

    st.markdown("### Comparison Chart")
    st.plotly_chart(
        build_money_bar_chart(
            labels + labels,
            values_a + values_b,
            f"{module} Comparison (A then B)",
        ),
        use_container_width=True,
    )
