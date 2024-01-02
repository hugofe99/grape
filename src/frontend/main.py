import streamlit as st
import streamlit.components.v1 as components

from src.backend.pdf import pdf_to_text
from src.backend.graphs.network import NetworkConstants

from src.frontend.resources.backend import title_to_paper_network


st.title("🍇 Grape")

st.header("Paper insights")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    with st.spinner("Analysing paper"):
        title = pdf_to_text.extract_title_from_pdf(pdf_file)
        st.markdown(f"### {title}")
        custom_config = st.toggle("custom graph config")
        paper_network = title_to_paper_network(title)
        paper_network.to_agraph_component(custom_config)
