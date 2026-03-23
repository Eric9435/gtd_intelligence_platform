import plotly.graph_objects as go


def build_compare_chart(metrics: list[str], values_a: list[float], values_b: list[float], label_a: str, label_b: str):
    fig = go.Figure()
    fig.add_bar(name=label_a, x=metrics, y=values_a)
    fig.add_bar(name=label_b, x=metrics, y=values_b)

    fig.update_layout(
        barmode="group",
        title=f"{label_a} vs {label_b}",
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
