import streamlit as st
from auth.roles import can_access_admin, can_edit, can_view


def require_login():
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to use the platform.")
        st.stop()


def require_view_access():
    role = st.session_state.get("role", "")
    if not can_view(role):
        st.error("You do not have permission to view this page.")
        st.stop()


def require_edit_access():
    role = st.session_state.get("role", "")
    if not can_edit(role):
        st.error("You do not have permission to edit or analyze data on this page.")
        st.stop()


def require_admin_access():
    role = st.session_state.get("role", "")
    if not can_access_admin(role):
        st.error("Admin access required.")
        st.stop()
