import streamlit as st
from auth.login import logout_user, is_logged_in


def render_sidebar_user_panel():
    if is_logged_in():
        st.sidebar.markdown("### User Session")
        st.sidebar.write(f"**Name:** {st.session_state.get('display_name', '-')}")
        st.sidebar.write(f"**Role:** {st.session_state.get('role', '-')}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
    else:
        st.sidebar.info("Not logged in.")
