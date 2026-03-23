import streamlit as st


def render_risk_summary_boxes(items: list[tuple[str, str]]):
    boxes_html = '<div class="risk-summary-grid">'
    for title, value in items:
        boxes_html += f"""
        <div class="risk-box">
            <div class="risk-box-title">{title}</div>
            <div class="risk-box-value">{value}</div>
        </div>
        """
    boxes_html += "</div>"

    st.markdown(boxes_html, unsafe_allow_html=True)
