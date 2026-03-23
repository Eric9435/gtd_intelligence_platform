import streamlit as st


def render_data_quality_panel(score: float, issues: list[str]):
    if score >= 90:
        badge = "badge badge-green"
        label = "HIGH"
    elif score >= 70:
        badge = "badge badge-yellow"
        label = "MEDIUM"
    else:
        badge = "badge badge-red"
        label = "LOW"

    st.markdown("### Data Quality")
    st.markdown(
        f"""
        <div class="section-card">
            <div style="margin-bottom:10px;">
                <span class="{badge}">{label}</span>
            </div>
            <div><b>Quality Score:</b> {score:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if issues:
        st.markdown("#### Validation / Anomaly Notes")
        for item in issues:
            st.write(f"- {item}")
    else:
        st.success("No validation or anomaly issues detected.")
