from semanticscholar.Paper import Paper as SemanticScholarPaper
from semanticscholar import SemanticScholar
from pyvis.network import Network


class Paper(SemanticScholarPaper):
    def __init__(
        self,
        title: str,
        semanticscholar_client: SemanticScholar | None = None,
        data: dict | None = None,
    ) -> None:
        if not semanticscholar_client:
            semanticscholar_client = SemanticScholar()

        self.semanticscholar_client = semanticscholar_client
        self._references_unique_ids = set()
        self._references_unique_titles = set()

        if not data:
            data = self._fetch_ssp_data(title)
        super().__init__(data)

    def _fetch_ssp_data(self, title: str) -> dict:
        search_results = self.semanticscholar_client.search_paper(query=title, limit=1)
        result_id = search_results[0]["paperId"]
        paper = self.semanticscholar_client.get_paper(result_id)
        return paper.raw_data

    def _is_good_reference(self, reference: SemanticScholarPaper) -> bool:
        if (
            reference.paperId and reference.paperId not in self._references_unique_ids
        ) and (
            reference.title and reference.title not in self._references_unique_titles
        ):
            self._references_unique_ids.add(reference.paperId)
            self._references_unique_titles.add(reference.title)
            return True
        else:
            return False

    def get_references(self) -> list[SemanticScholarPaper]:
        return [
            reference
            for reference in self.references
            if self._is_good_reference(reference)
        ]
