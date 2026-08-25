"""
WatchSphere AI v3.0 - CSS Injection Loader Utility
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from pathlib import Path
import streamlit as st


def load_css(css_file_path: str = "assets/css/style.css") -> None:
    """
    Reads local CSS file and injects custom styles into Streamlit document head.
    """
    path = Path(css_file_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS styling asset not found at '{css_file_path}'")
