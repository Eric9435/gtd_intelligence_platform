import plotly.graph_objects as go


def build_myanmar_asset_map():
    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            lon=[96.1951, 96.0891, 95.9560],
            lat=[16.8661, 21.9588, 19.7633],
            text=["Yangon", "Mandalay", "Naypyidaw"],
            mode="markers+text",
            textposition="top center",
            marker=dict(size=10),
            name="Key Zones",
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
        title="Myanmar GT&D Starter Map",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig
