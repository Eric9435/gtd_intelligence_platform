import streamlit as st

from ui.components.header import render_header
from auth.login import login_user


def render_login_page():
    render_header(
        "Login",
        "Please sign in to access the GT&D Intelligence Platform.",
    )

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if login_user(username, password):
            st.success("Login successful. Please choose a page from the sidebar.")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown("### Demo Accounts")
    st.write("- admin / admin123")
    st.write("- engineer / engineer123")
    st.write("- viewer / viewer123")
