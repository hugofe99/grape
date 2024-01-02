from semanticscholar import SemanticScholar
import streamlit as st


@st.cache_resource(show_spinner=False)
def get_semanticscholar_client():
    return SemanticScholar()
