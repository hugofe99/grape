from dataclasses import dataclass, field


@dataclass
class TitleCandidate:
    text: str
    font_size: int
    dist_from_top: int
    score: float = field(init=False)

    def __post_init__(self):
        self.text = self.text.strip()
        self.font_size = int(self.font_size)
        self.dist_from_top = int(self.dist_from_top)
        self.score = self._get_score()

    def _get_score(self) -> float:
        MIDDLE_OF_PAGE = 400
        POSITION_WEIGHT = 1 / 100
        score = self.font_size + POSITION_WEIGHT * (MIDDLE_OF_PAGE - self.dist_from_top)
        return score

    def is_similar(self, other: "TitleCandidate") -> bool:
        TOL_SIZE = 1
        TOL_SCORE = 5
        if (
            (abs(self.font_size - other.font_size) <= TOL_SIZE)
            and (abs(self.score - other.score) <= TOL_SCORE)
            and (self.text != other.text)
        ):
            return True
        else:
            return False

    def __repr__(self) -> str:
        s = f"TitleCandidate:\ntext={self.text}\nfont size={self.font_size}\ndist from top={self.dist_from_top}\nscore={self.score}\n"
        return s
