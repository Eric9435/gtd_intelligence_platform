import streamlit as st

from storage.db import init_db
from auth.login import init_auth_state, is_logged_in
from auth.permissions import require_login, require_view_access
from ui.components.header import load_custom_css
from ui.components.sidebar import render_sidebar_user_panel
from ui.pages.login import render_login_page
from ui.pages.home import render_home_page
from ui.pages.executive_summary import render_executive_summary_page
from ui.pages.dashboard import render_dashboard_page
from ui.pages.generation import render_generation_page
from ui.pages.transmission import render_transmission_page
from ui.pages.distribution import render_distribution_page
from ui.pages.sales import render_sales_page
from ui.pages.roi import render_roi_page
from ui.pages.export import render_export_page
from ui.pages.forecast import render_forecast_page
from ui.pages.scenario import render_scenario_page
from ui.pages.map import render_map_page
from ui.pages.history import render_history_page
from ui.pages.compare import render_compare_page
from ui.pages.reports import render_reports_page
from ui.pages.admin import render_admin_page


def main():
    st.set_page_config(
        page_title="GT&D Intelligence Platform",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_db()
    init_auth_state()
    load_custom_css()

    render_sidebar_user_panel()

    if not is_logged_in():
        render_login_page()
        return

    require_login()
    require_view_access()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Executive Summary",
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
            "Compare",
            "Reports",
            "Admin",
        ],
    )

    if page == "Home":
        render_home_page()
    elif page == "Executive Summary":
        render_executive_summary_page()
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
    elif page == "Compare":
        render_compare_page()
    elif page == "Reports":
        render_reports_page()
    elif page == "Admin":
        render_admin_page()


if __name__ == "__main__":
    main()
