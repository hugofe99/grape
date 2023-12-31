import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network

def get_trivial_graph_html() -> str:
    graph = nx.Graph()
    graph.add_node("Node A")
    graph.add_node("Node B")
    graph.add_edge("Node A", "Node B")

    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(graph)
    html = net.generate_html()
    return html

