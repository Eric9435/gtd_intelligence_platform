import plotly.graph_objects as go
from core.geo.geo_loader import load_csv_points


def build_myanmar_asset_map():
    generation_rows = load_csv_points("data/geo/generation_sites.csv")
    substation_rows = load_csv_points("data/geo/substations.csv")

    fig = go.Figure()

    if generation_rows:
        fig.add_trace(
            go.Scattergeo(
                lon=[float(r["lon"]) for r in generation_rows if r.get("lon")],
                lat=[float(r["lat"]) for r in generation_rows if r.get("lat")],
                text=[f"{r.get('name', 'Plant')} ({r.get('type', 'Unknown')})" for r in generation_rows],
                mode="markers+text",
                textposition="top center",
                marker=dict(size=10, color="cyan", symbol="circle"),
                name="Generation Sites",
            )
        )

    if substation_rows:
        fig.add_trace(
            go.Scattergeo(
                lon=[float(r["lon"]) for r in substation_rows if r.get("lon")],
                lat=[float(r["lat"]) for r in substation_rows if r.get("lat")],
                text=[f"{r.get('name', 'Substation')} ({r.get('voltage_level', 'N/A')})" for r in substation_rows],
                mode="markers+text",
                textposition="bottom center",
                marker=dict(size=8, color="orange", symbol="square"),
                name="Substations",
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
        title="Myanmar GT&D Asset Map",
        height=540,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
