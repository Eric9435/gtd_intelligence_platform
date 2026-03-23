import streamlit as st

from storage.db import init_db
from ui.components.header import load_custom_css
from ui.pages.home import render_home_page
from ui.pages.dashboard import render_dashboard_page
from ui.pages.generation import render_generation_page
from ui.pages.transmission import render_transmission_page
from ui.pages.distribution import render_distribution_page
from ui.pages.sales import render_sales_page
from ui.pages.roi import render_roi_page
from ui.pages.export import render_export_page
from ui.pages.map import render_map_page
from ui.pages.history import render_history_page
from ui.pages.forecast import render_forecast_page
from ui.pages.scenario import render_scenario_page
from ui.pages.reports import render_reports_page


def main():
    st.set_page_config(
        page_title="GT&D Intelligence Platform",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_db()
    load_custom_css()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Dashboard",
            "Generation",
            "Transmission",
            "Distribution",
            "Sales",
            "ROI",
            "Export",
            "Forecast",
            "Scenario",
            "Map",
            "History",
            "Reports",
        ],
    )

    if page == "Home":
        render_home_page()
    elif page == "Dashboard":
        render_dashboard_page()
    elif page == "Generation":
        render_generation_page()
    elif page == "Transmission":
        render_transmission_page()
    elif page == "Distribution":
        render_distribution_page()
    elif page == "Sales":
        render_sales_page()
    elif page == "ROI":
        render_roi_page()
    elif page == "Export":
        render_export_page()
    elif page == "Forecast":
        render_forecast_page()
    elif page == "Scenario":
        render_scenario_page()
    elif page == "Map":
        render_map_page()
    elif page == "History":
        render_history_page()
    elif page == "Reports":
        render_reports_page()


if __name__ == "__main__":
    main()
