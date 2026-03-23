import plotly.graph_objects as go
from core.geo.geo_loader import load_csv_points


def _risk_color(level: str) -> str:
    level = str(level).upper()
    if level == "CRITICAL":
        return "red"
    if level == "HIGH":
        return "orange"
    if level == "WARNING":
        return "yellow"
    return "green"


def build_myanmar_risk_map():
    rows = load_csv_points("data/geo/demand_zones.csv")

    if not rows:
        rows = [
            {"name": "Yangon", "lat": 16.8661, "lon": 96.1951, "risk_level": "CRITICAL"},
            {"name": "Mandalay", "lat": 21.9588, "lon": 96.0891, "risk_level": "HIGH"},
            {"name": "Naypyidaw", "lat": 19.7633, "lon": 95.9560, "risk_level": "WARNING"},
        ]

    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            lon=[float(r["lon"]) for r in rows],
            lat=[float(r["lat"]) for r in rows],
            text=[f"{r.get('name', 'Zone')} - {r.get('risk_level', 'NORMAL')}" for r in rows],
            mode="markers+text",
            textposition="top center",
            marker=dict(
                size=[18 if str(r.get("risk_level", "")).upper() == "CRITICAL" else 14 for r in rows],
                color=[_risk_color(r.get("risk_level", "NORMAL")) for r in rows],
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
        height=540,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
