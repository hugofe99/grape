import streamlit as st
from streamlit.components.v1.components import CustomComponent

from src.backend.papers.paper import Paper
from src.backend.graphs.network import PaperNetwork

from src.frontend.resources.clients import get_semanticscholar_client


@st.cache_data(show_spinner=False)
def title_to_paper_network(title: str) -> PaperNetwork:
    paper = Paper(title, semanticscholar_client=get_semanticscholar_client())
    network = PaperNetwork(paper)
    return network
