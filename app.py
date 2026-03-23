import streamlit as st

from storage.db import init_db
from ui.components.header import load_custom_css
from ui.pages.home import render_home_page
from ui.pages.transmission import render_transmission_page
from ui.pages.generation import render_generation_page
from ui.pages.distribution import render_distribution_page
from ui.pages.map import render_map_page
from ui.pages.history import render_history_page


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
        ["Home", "Generation", "Transmission", "Distribution", "Map", "History"],
    )

    if page == "Home":
        render_home_page()
    elif page == "Generation":
        render_generation_page()
    elif page == "Transmission":
        render_transmission_page()
    elif page == "Distribution":
        render_distribution_page()
    elif page == "Map":
        render_map_page()
    elif page == "History":
        render_history_page()


if __name__ == "__main__":
    main()
