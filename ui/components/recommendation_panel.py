import streamlit as st


def render_recommendation_panel(title: str, recommendations: list[str]):
    st.markdown(
        f"""
        <div class="ai-card fade-in">
            <div class="ai-title">{title}</div>
        """,
        unsafe_allow_html=True,
    )

    for rec in recommendations:
        st.markdown(
            f'<div class="ai-item">• {rec}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
