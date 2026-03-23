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
