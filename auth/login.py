import streamlit as st

DEMO_USERS = {
    "admin": {
        "password": "admin123",
        "role": "ADMIN",
        "display_name": "System Admin",
    },
    "engineer": {
        "password": "engineer123",
        "role": "ENGINEER",
        "display_name": "Grid Engineer",
    },
    "viewer": {
        "password": "viewer123",
        "role": "VIEWER",
        "display_name": "Executive Viewer",
    },
}


def init_auth_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "display_name" not in st.session_state:
        st.session_state.display_name = ""


def login_user(username: str, password: str) -> bool:
    user = DEMO_USERS.get(username)
    if not user:
        return False
    if user["password"] != password:
        return False

    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.role = user["role"]
    st.session_state.display_name = user["display_name"]
    return True


def logout_user():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.display_name = ""


def is_logged_in() -> bool:
    return bool(st.session_state.get("authenticated", False))
