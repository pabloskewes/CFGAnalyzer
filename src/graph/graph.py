from typing import Any, List, Dict, Tuple
from dataclasses import dataclass

import graphviz
from IPython.display import Image



class GraphError(Exception):
    """An exception raised when an invalid operation is performed on a graph."""

    pass


@dataclass
class GraphSettings:
    """Settings for the graph."""

    allow_adding_existing_nodes: bool = False
    allow_adding_edges_to_non_existing_nodes: bool = False


class Graph:
    """A graph data structure. Can be initialized from nodes and edges, an adjacency list, or an adjacency matrix."""

    def __init__(self):
        self.nodes: List[Any] = []
        self.edges: List[Tuple[Any, Any]] = []
        self._adjacency_list: Dict[Any, List[Any]] = {}
        self._adjacency_matrix: List[List[int]] = []
        self.settings = GraphSettings()

    def add_node(self, node: Any):
        """Add a node to the graph."""
        if node in self.nodes:
            if not self.settings.allow_adding_existing_nodes:
                raise GraphError(f"Node {node} already exists in the graph.")
            return
        self.nodes.append(node)
        self._reset()

    def add_edge(self, source: Any, target: Any):
        """Add an edge to the graph."""
        if (
            source not in self.nodes
            and not self.settings.allow_adding_edges_to_non_existing_nodes
        ):
            raise GraphError(f"Node {source} does not exist in the graph.")
        if (
            target not in self.nodes
            and not self.settings.allow_adding_edges_to_non_existing_nodes
        ):
            raise GraphError(f"Node {target} does not exist in the graph.")
        self.edges.append((source, target))
        self._reset()

    def _reset(self):
        """Reset the adjacency list and adjacency matrix."""
        self._adjacency_list = {}
        self._adjacency_matrix = []
        
    def validate(self) -> bool:
        """Validate the graph."""
        for source, target in self.edges:
            if source not in self.nodes or target not in self.nodes:
                return False
        return True

    @property
    def num_nodes(self) -> int:
        return len(self.nodes)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    @property
    def adjacency_list(self) -> Dict[Any, List[Any]]:
        if not self._adjacency_list:
            self._calculate_adjacency_list()
        return self._adjacency_list

    @property
    def adjacency_matrix(self) -> List[List[int]]:
        if not self._adjacency_matrix:
            self._calculate_adjacency_matrix()
        return self._adjacency_matrix

    def _calculate_adjacency_list(self):
        self._adjacency_list = {}
        for node in self.nodes:
            self._adjacency_list[node] = []
        for edge in self.edges:
            source, target = edge
            self._adjacency_list[source].append(target)

    def _calculate_adjacency_matrix(self):
        num_nodes = len(self.nodes)
        self._adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]
        for edge in self.edges:
            source, target = edge
            source_index = self.nodes.index(source)
            target_index = self.nodes.index(target)
            self._adjacency_matrix[source_index][target_index] = 1

    @classmethod
    def from_nodes_and_edges(
        cls, nodes: List[Any], edges: List[Tuple[Any, Any]]
    ) -> "Graph":
        """
        Initialize a graph from nodes and edges.
        Args:
            nodes: A list of nodes.
            edges: A list of edges, where each edge is a tuple of two nodes.
        Returns:
            An instance of Graph.
        """
        graph = cls()
        for node in nodes:
            graph.add_node(node)
        for edge in edges:
            source, target = edge
            graph.add_edge(source, target)
        return graph

    @classmethod
    def from_adjacency_list(cls, adjacency_list: Dict[Any, List[Any]]) -> "Graph":
        """
        Initialize a graph from an adjacency list.
        Args:
            adjacency_list: A dictionary where the keys are nodes and the values are lists of neighbors.
        Returns:
            An instance of Graph.
        """
        graph = cls()
        for node, neighbors in adjacency_list.items():
            if node not in graph.nodes:
                graph.add_node(node)
            for neighbor in neighbors:
                if neighbor not in graph.nodes:
                    graph.add_node(neighbor)
                graph.add_edge(node, neighbor)
        return graph

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix: List[List[int]]) -> "Graph":
        """
        Initialize a graph from an adjacency matrix.
        Args:
            adjacency_matrix: A list of lists of integers, where each integer is either 0 or 1.
        Returns:
            An instance of Graph.
        """
        graph = cls()
        for row_index, row in enumerate(adjacency_matrix):
            node = row_index
            if node not in graph.nodes:
                graph.add_node(node)
            for col_index, has_edge in enumerate(row):
                if has_edge:
                    neighbor = col_index
                    if neighbor not in graph.nodes:
                        graph.add_node(neighbor)
                    graph.add_edge(node, neighbor)
        return graph
    
    def plot(self):
        """Plot the graph using Graphviz."""
        dot = graphviz.Digraph()

        # Add nodes
        for node in self.nodes:
            dot.node(str(node))

        # Add edges
        for edge in self.edges:
            dot.edge(str(edge[0]), str(edge[1]))

        # Set the node at the top of the figure
        dot.graph_attr['rankdir'] = 'TB'

        src = graphviz.Source(dot.source)
        src.format = 'png'  # Output format (change it if needed)
        src.render('graph')  # Output file name (change it if needed)
        display(Image(filename='graph.png'))
        # src.view()  # Display the graph directly in Jupyter Notebook

    # def plot(self, top_node: Any = None):
    #     """Plot the graph using networkx and matplotlib."""
    #     nx_graph = nx.DiGraph(directed=True)
    #     nx_graph.add_nodes_from(self.nodes)
    #     nx_graph.add_edges_from(self.edges)

    #     pos = nx.spring_layout(nx_graph)
        
    #     pos[top_node] = (pos[top_node][0], 1.0)

    #     node_size = 2000
    #     node_color = "lightblue"

    #     nx.draw_networkx_nodes(
    #         nx_graph, pos, node_size=node_size, node_color=node_color, node_shape="s"
    #     )
    #     nx.draw_networkx_labels(nx_graph, pos, font_size=10, verticalalignment="center")

    #     nx.draw_networkx_edges(
    #         nx_graph,
    #         pos,
    #         arrows=True,
    #         arrowstyle="->",
    #         arrowsize=20,
    #         edge_color="black",
    #     )

    #     plt.xlim(-1.1, 1.1)
    #     plt.ylim(-1.1, 1.1)
    #     plt.axis("off")

    #     plt.show()


def ciclomatic_complexity(graph: Graph) -> int:
    """Calculate the ciclomatic complexity of a graph."""
    P = 1
    return graph.num_edges - graph.num_nodes + 2 * P
