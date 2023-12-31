from PyPDF2 import PdfReader
from io import BytesIO
import re


def pdf_to_text(file: BytesIO) -> str:
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


def text_to_reference_section(text: str) -> str | None:
    references_pattern = re.compile(r"References|Bibliography|Works Cited", re.IGNORECASE)
    match = references_pattern.search(text)
    if match:
        references_start = match.end()
        references_section = text[references_start:]
        return references_section.strip()
    else:
        return None
    
def reference_section_to_references(text: str):
    pat = r"\[\d+]"
    pass