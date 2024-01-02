import streamlit as st
import streamlit.components.v1 as components

from src.backend.pdf import pdf_to_text
from src.backend.papers.paper import Paper
from src.backend.graphs.network import PaperNetwork, NetworkConstants

from src.frontend.resources.backend import paper_title_to_network_html

st.title("🍇 Grape")

st.header("Paper insights")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    with st.spinner("Analysing paper"):
        title = pdf_to_text.extract_title_from_pdf(pdf_file)
        html = paper_title_to_network_html(title)
        st.markdown(f"### {title}")
        components.html(
            html, height=NetworkConstants._HEIGHT_INT, width=NetworkConstants._WIDTH_INT
        )
