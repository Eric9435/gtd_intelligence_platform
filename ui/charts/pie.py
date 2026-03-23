import plotly.graph_objects as go


def build_loss_pie_chart(technical_loss: float, non_technical_loss: float):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Technical Loss", "Non-Technical Loss"],
                values=[technical_loss, non_technical_loss],
                hole=0.4,
            )
        ]
    )
    fig.update_layout(title="Loss Breakdown", height=350, margin=dict(l=20, r=20, t=50, b=20))
    return fig
