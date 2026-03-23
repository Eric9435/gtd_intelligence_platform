import streamlit as st


def render_risk_badge(level: str):
    level = level.upper()

    if level in ["CRITICAL", "HIGH"]:
        cls = "badge badge-red"
    elif level == "WARNING":
        cls = "badge badge-yellow"
    else:
        cls = "badge badge-green"

    st.markdown(
        f'<span class="{cls}">{level}</span>',
        unsafe_allow_html=True,
    )
