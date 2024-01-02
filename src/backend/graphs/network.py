from pyvis.network import Network
import networkx as nx
from src.backend.papers.paper import Paper
from src.backend.graphs.config import get_default_network, NetworkConstants
from semanticscholar.Paper import Paper as SemanticScholarPaper
from streamlit_agraph import agraph, Config, Node, Edge, ConfigBuilder
from streamlit.components.v1.components import CustomComponent
import math


class PaperNetwork:
    def __init__(
        self,
        paper: Paper,
        _network: Network | None = None,
        _network_constants: NetworkConstants = NetworkConstants,
    ) -> None:
        if not _network:
            _network = get_default_network(_network_constants)

        self.network_constants = _network_constants
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
        def multiline_text(text: str, _words_per_line: int = _words_per_line):
            if not text:
                return ""
            multiline_text = []
            for i, word in enumerate(text.split(), start=1):
                multiline_text.append(word)
                if i % _words_per_line == 0:
                    multiline_text.append("\n")
            return " ".join(multiline_text)

        title = multiline_text(paper.title)
        abstract = multiline_text(paper.abstract)
        paper_id = paper.paperId
        authors = multiline_text(
            ", ".join([author["name"] for author in paper.authors])
        )
        year = paper.year
        citation_count = paper.citationCount

        description = f"Title:{title}\nPaper ID:{paper_id}\nAuthors:{authors}\nYear:{year}\nCitation Count:{citation_count}\nAbstract:\n{abstract}"
        return description

    def _generate_network(self) -> None:
        if self.network.num_nodes():
            return

        self.network.add_node(
            n_id=self.paper.paperId,
            label=self.paper.title,
            title=self._paper_to_description(self.paper),
            size=math.log(self.paper.citationCount + 2) * 2,
        )

        for ref in self.paper.get_references():
            self.network.add_node(
                n_id=ref.paperId,
                label=f"{ref.title[:10]}...",
                title=self._paper_to_description(ref),
                size=math.log(ref.citationCount + 2),
            )
            self.network.add_edge(
                source=ref.paperId,
                to=self.paper.paperId,
                # label='is_ref_to'
            )

    def to_agraph_component(self, custom_config: bool = False) -> CustomComponent:
        nodes, edges, _, _, _, _ = self.network.get_network_data()

        def format_node(node_dict: dict) -> dict:
            return node_dict

        def format_edge(edge_dict: dict) -> dict:
            edge_dict["source"] = edge_dict.pop("from")
            edge_dict["target"] = edge_dict.pop("to")
            return edge_dict

        nodes = [Node(**format_node(node)) for node in nodes]
        edges = [Edge(**format_edge(edge)) for edge in edges]

        if custom_config:
            config_builder = ConfigBuilder(nodes, edges)
            config = config_builder.build()
        else:
            config = Config()

        return agraph(nodes, edges, config)

    def to_networkx_graph(self) -> nx.Graph:
        """Could be useful for obsidian integration?"""
        raise NotImplementedError()
