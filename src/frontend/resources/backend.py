import streamlit as st

from src.backend.papers.paper import Paper
from src.backend.graphs.network import PaperNetwork

from src.frontend.resources.clients import get_semanticscholar_client


@st.cache_data(show_spinner=False)
def paper_title_to_network_html(title: str) -> str:
    paper = Paper(title, semanticscholar_client=get_semanticscholar_client())
    network = PaperNetwork(paper)
    html = network.html
    return html
