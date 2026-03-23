import plotly.graph_objects as go


def build_temp_chart(oil: float, winding: float):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=["Oil Temp", "Winding Temp"],
            y=[oil, winding],
            mode="lines+markers",
            name="Temperature",
        )
    )

    fig.update_layout(
        title="Temperature Profile",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def build_export_line_chart(labels: list[str], values: list[float], title: str):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=values,
            mode="lines+markers",
            name=title,
        )
    )

    fig.update_layout(
        title=title,
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
