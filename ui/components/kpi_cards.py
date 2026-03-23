import streamlit as st


def get_status_class(value: float) -> str:
    if value >= 80:
        return "status-critical"
    elif value >= 60:
        return "status-warning"
    return "status-normal"


def render_kpi_cards(result: dict):
    cols = st.columns(4)

    cards = [
        ("Loading (%)", result["loading_pct"]),
        ("Risk Score", result["risk_score"]),
        ("Avg Current (A)", result["avg_current"]),
        ("Imbalance (%)", result["imbalance_pct"]),
    ]

    for col, (label, value) in zip(cols, cards):
        status = get_status_class(float(value))
        col.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-value {status}">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    cols2 = st.columns(3)

    cards2 = [
        ("Voltage Dev (%)", result["voltage_dev_pct"]),
        ("Oil Temp (°C)", result["oil_temp"]),
        ("Winding Temp (°C)", result["winding_temp"]),
    ]

    for col, (label, value) in zip(cols2, cards2):
        status = get_status_class(float(value))
        col.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-value {status}">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )