import streamlit as st
import pandas as pd

from ui.components.header import render_header
from core.forecast.demand import forecast_next_demand
from core.forecast.generation import forecast_next_generation
from ui.charts.trend import build_forecast_trend_chart


def render_forecast_page():
    render_header(
        "Forecast",
        "Forecast demand growth and generation derating trends.",
    )

    col1, col2 = st.columns(2)

    with col1:
        current_demand_mw = st.number_input("Current Demand (MW)", value=3600.0)
        demand_growth_pct = st.number_input("Demand Growth (%)", value=4.0)

    with col2:
        current_generation_mw = st.number_input("Current Generation (MW)", value=4200.0)
        generation_derating_pct = st.number_input("Generation Derating (%)", value=1.5)

    periods = st.slider("Forecast Months", min_value=3, max_value=12, value=6)

    if st.button("Run Forecast"):
        demand_data = forecast_next_demand(current_demand_mw, demand_growth_pct, periods)
        generation_data = forecast_next_generation(current_generation_mw, generation_derating_pct, periods)

        demand_df = pd.DataFrame(demand_data)
        generation_df = pd.DataFrame(generation_data)

        st.markdown("### Demand Forecast")
        st.dataframe(demand_df, use_container_width=True)
        st.plotly_chart(
            build_forecast_trend_chart(
                demand_df["period"].tolist(),
                demand_df["forecast_demand_mw"].tolist(),
                "Demand Forecast",
                "MW",
            ),
            use_container_width=True,
        )

        st.markdown("### Generation Forecast")
        st.dataframe(generation_df, use_container_width=True)
        st.plotly_chart(
            build_forecast_trend_chart(
                generation_df["period"].tolist(),
                generation_df["forecast_generation_mw"].tolist(),
                "Generation Forecast",
                "MW",
            ),
            use_container_width=True,
        )
