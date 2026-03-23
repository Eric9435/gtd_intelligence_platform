import streamlit as st


def render_animated_status_box(title: str, value: str, level: str):
    if level in ["CRITICAL", "HIGH"]:
        glow = "kpi-glow-red pulse-risk"
    elif level == "WARNING":
        glow = "kpi-glow-yellow"
    else:
        glow = "kpi-glow-green"

    st.markdown(
        f"""
        <div class="kpi-card float-card {glow}">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
