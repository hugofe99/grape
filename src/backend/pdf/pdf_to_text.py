from io import BytesIO
import pdfplumber
from pathlib import Path
from src.backend.pdf.models import TitleCandidate


def extract_title_from_pdf(pdf: BytesIO | Path | pdfplumber.PDF) -> str:
    if not isinstance(pdf, pdfplumber.PDF):
        with pdfplumber.open(pdf) as pdf:
            return extract_title_from_pdf(pdf)

    title_candidates = extract_title_candidates(pdf)
    best_candidate = get_best_title_candidate(title_candidates)
    return best_candidate.text


def extract_title_candidates(
    pdf: pdfplumber.PDF, _check_n_pages: int = 3
) -> list[TitleCandidate]:
    title_candidates = []
    for page in pdf.pages[:_check_n_pages]:
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
    return title_candidates


def get_best_title_candidate(
    list_of_title_candidates: list[TitleCandidate], _top_n: int = 5
) -> TitleCandidate:
    top_candidates = sorted(
        list_of_title_candidates, key=lambda x: x.score, reverse=True
    )[:_top_n]
    start_of_title = top_candidates[0]
    full_title_candidates = [start_of_title] + [
        candidate
        for candidate in list_of_title_candidates
        if candidate.is_similar(start_of_title)
    ]
    best_title_candidate = TitleCandidate(
        text=" ".join(cand.text for cand in full_title_candidates),
        font_size=start_of_title.font_size,
        dist_from_top=start_of_title.dist_from_top,
    )
    return best_title_candidate
