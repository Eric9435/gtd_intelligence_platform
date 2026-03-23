import plotly.graph_objects as go


def build_myanmar_risk_map():
    names = ["Yangon", "Mandalay", "Naypyidaw", "Bago", "Magway"]
    lons = [96.1951, 96.0891, 95.9560, 96.4910, 94.9320]
    lats = [16.8661, 21.9588, 19.7633, 17.3360, 20.1490]
    levels = ["CRITICAL", "HIGH", "WARNING", "NORMAL", "WARNING"]

    colors = []
    for level in levels:
        if level == "CRITICAL":
            colors.append("red")
        elif level == "HIGH":
            colors.append("orange")
        elif level == "WARNING":
            colors.append("yellow")
        else:
            colors.append("green")

    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            lon=lons,
            lat=lats,
            text=[f"{n} - {lvl}" for n, lvl in zip(names, levels)],
            mode="markers+text",
            textposition="top center",
            marker=dict(
                size=[18, 16, 14, 12, 14],
                color=colors,
                line=dict(width=1, color="white"),
            ),
            name="Risk Zones",
        )
    )

    fig.update_geos(
        scope="asia",
        showcountries=True,
        countrycolor="gray",
        showland=True,
        landcolor="#0f172a",
        coastlinecolor="gray",
        projection_type="natural earth",
        lataxis_range=[9, 29],
        lonaxis_range=[92, 102],
    )

    fig.update_layout(
        title="Myanmar GT&D Risk Map",
        height=520,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
