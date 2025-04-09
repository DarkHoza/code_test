# utils.py
import streamlit as st

def hide_sidebar_pages():
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
                                                         