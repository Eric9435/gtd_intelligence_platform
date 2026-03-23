import plotly.graph_objects as go


def build_risk_gauge(value: float):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": (
                        "red" if value >= 80
                        else "orange" if value >= 60
                        else "gold" if value >= 30
                        else "green"
                    )
                },
                "steps": [
                    {"range": [0, 30], "color": "#1f7a1f"},
                    {"range": [30, 60], "color": "#d4a017"},
                    {"range": [60, 80], "color": "#d97706"},
                    {"range": [80, 100], "color": "#b91c1c"},
                ],
            },
        )
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig
