import plotly.graph_objects as go


def build_generation_capacity_chart(actual_generation: float, available_capacity: float, installed_capacity: float):
    fig = go.Figure()
    fig.add_bar(name="Actual Generation", x=["Plant"], y=[actual_generation])
    fig.add_bar(name="Available Capacity", x=["Plant"], y=[available_capacity])
    fig.add_bar(name="Installed Capacity", x=["Plant"], y=[installed_capacity])

    fig.update_layout(
        barmode="group",
        title="Generation vs Available vs Installed",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
