import streamlit as st
from pathlib import Path


def load_custom_css():
    css_paths = [
        Path("assets/styles/custom.css"),
        Path("assets/styles/animations.css"),
    ]
    for css_path in css_paths:
        if css_path.exists():
            st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def render_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-card fade-in">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
