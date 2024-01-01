from PyPDF2 import PdfReader
from io import BytesIO
import re
import pdfplumber
from dataclasses import dataclass, asdict, field
from pprint import pprint
from typing import List


@dataclass
class TitleCandidate:
    text: str
    font_size: str
    dist_from_top: float
    score: float = field(init=False)

    def __post_init__(self):
        MIDDLE_OF_PAGE = 400
        POSITION_WEIGHT = 1 / 100
        self.score = self.font_size + POSITION_WEIGHT * (
            MIDDLE_OF_PAGE - self.dist_from_top
        )


def get_best_title_candidate(
    list_of_title_candidates: List[TitleCandidate], _top_n: int = 5
) -> TitleCandidate:
    top_candidates = sorted(
        list_of_title_candidates, key=lambda x: x.score, reverse=True
    )[:_top_n]
    return top_candidates[0]


def extract_title_from_pdf(pdf_file: BytesIO | pdfplumber.PDF) -> str:
    if not isinstance(pdf_file, pdfplumber.PDF):
        pass

    title_candidates = []
    for page in pdf_file.pages[:3]:
        text_lines = page.extract_text_lines()
        for text_line in text_lines:
            title_candidates.append(
                TitleCandidate(
                    text=text_line["text"],
                    font_size=sum(char["size"] for char in text_line["chars"])
                    / len(text_line["chars"]),
                    dist_from_top=text_line["top"],
                )
            )
    best_candidate = get_best_title_candidate(title_candidates)
    return best_candidate.text


with pdfplumber.open("atari_drl.pdf") as file:
    title = extract_title_from_pdf(file)
    print(title)


def pdf_to_text(file: BytesIO) -> str:
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


def text_to_reference_section(text: str) -> str | None:
    references_pattern = re.compile(
        r"References|Bibliography|Works Cited", re.IGNORECASE
    )
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
