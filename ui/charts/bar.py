import plotly.graph_objects as go


def build_load_chart(load: float, capacity: float):
    fig = go.Figure()

    fig.add_bar(name="Load (MW)", x=["System"], y=[load])
    fig.add_bar(name="Capacity (MVA)", x=["System"], y=[capacity])

    fig.update_layout(
        barmode="group",
        title="Load vs Capacity",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig
