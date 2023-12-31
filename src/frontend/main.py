import streamlit as st
import streamlit.components.v1 as components

from src.backend.trivial_graph import get_trivial_graph_html
from src.backend.pdf_to_text import pdf_to_text, text_to_reference_section


st.title("🍇 Grape")

st.header("PDF Text Extractor")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    with st.spinner("Extracting text..."):
        text = pdf_to_text(pdf_file)
    ref_sec = text_to_reference_section(text)
    st.subheader("Reference section?")
    st.text(ref_sec)


st.markdown(
    """ ___ """
)

components.html(get_trivial_graph_html(), height=500)
