from pyvis.network import Network
import networkx as nx
from src.backend.papers.paper import Paper
from semanticscholar.Paper import Paper as SemanticScholarPaper


class NetworkConstants:
    HEIGHT = "750px"
    WIDTH = "750px"
    DIRECTED = False
    NOTEBOOK = False
    BACKGROUND_COLOUR = "#0E1117"
    FONT_COLOUR = "white"

    PAPER_SIZE = 20
    REF_SIZE = 10

    _HEIGHT_INT = int(HEIGHT.split("px")[0])
    _WIDTH_INT = int(WIDTH.split("px")[0])


def get_default_network(
    _network_constants: NetworkConstants = NetworkConstants(),
) -> Network:
    return Network(
        height=_network_constants.HEIGHT,
        width=_network_constants.WIDTH,
        directed=_network_constants.DIRECTED,
        notebook=_network_constants.NOTEBOOK,
        bgcolor=_network_constants.BACKGROUND_COLOUR,
        font_color=_network_constants.FONT_COLOUR,
    )


class PaperNetwork:
    def __init__(self, paper: Paper, _network: Network | None = None) -> None:
        if not _network:
            _network = get_default_network()

        self.paper = paper
        self.network = _network
        self.html: str = ""

        self.__post_init__()

    def __post_init__(self) -> None:
        self._generate_network()
        self.html = self.network.generate_html()

    def _paper_to_description(
        self, paper: Paper | SemanticScholarPaper, _words_per_line: int = 9
    ) -> str:
        def multiline_text(text: str, _words_per_line: int):
            if not text:
                return ""
            multiline_text = []
            for i, word in enumerate(text.split(), start=1):
                multiline_text.append(word)
                if i % _words_per_line == 0:
                    multiline_text.append("\n")
            return " ".join(multiline_text)

        title = paper.title
        abstract = multiline_text(paper.abstract, _words_per_line)
        paper_id = paper.paperId
        authors = multiline_text(
            ", ".join([author["name"] for author in paper.authors]), _words_per_line
        )
        year = paper.year
        citation_count = paper.citationCount

        description = f"Title:\n{title}\nAbstract:\n{abstract}\n\nPaper ID: {paper_id}\nAuthors: {authors}\nYear: {year}\nCitation Count: {citation_count}"
        return description

    def _generate_network(self) -> None:
        if self.network.num_nodes():
            return

        self.network.add_node(
            n_id=self.paper.paperId,
            label=self.paper.title,
            title=self._paper_to_description(self.paper),
            size=NetworkConstants.PAPER_SIZE,
        )

        for ref in self.paper.get_references():
            self.network.add_node(
                n_id=ref.paperId,
                label=f"{ref.title[:10]}...",
                title=self._paper_to_description(ref),
                size=NetworkConstants.REF_SIZE,
            )
            self.network.add_edge(source=ref.paperId, to=self.paper.paperId)

    def to_networkx_graph(self) -> nx.Graph:
        """Could be useful for obsidian integration?"""
        raise NotImplementedError()
