from typing import Any, List, Dict, Tuple


class Graph:
    
    def __init__(self):
        self.nodes: List[Any] = []
        self.edges: List[tuple[Any, Any]] = []
        self._adjacency_list: Dict[Any, List[Any]] = {}
        self._adjacency_matrix: List[List[int]] = []

    def add_node(self, node: Any):
        self.nodes.append(node)

    def add_edge(self, source: Any, target: Any):
        self.edges.append((source, target))
        
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
    def from_nodes_and_edges(cls, nodes: List[Any], edges: List[Tuple[Any, Any]]) -> 'Graph':
        graph = cls()
        for node in nodes:
            graph.add_node(node)
        for edge in edges:
            source, target = edge
            graph.add_edge(source, target)
        return graph

    @classmethod
    def from_adjacency_list(cls, adjacency_list: Dict[Any, List[Any]]) -> 'Graph':
        graph = cls()
        for node, neighbors in adjacency_list.items():
            graph.add_node(node)
            for neighbor in neighbors:
                graph.add_edge(node, neighbor)
        return graph

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix: List[List[int]]) -> 'Graph':
        graph = cls()
        for row_index, row in enumerate(adjacency_matrix):
            node = row_index
            graph.add_node(node)
            for col_index, has_edge in enumerate(row):
                if has_edge:
                    neighbor = col_index
                    graph.add_edge(node, neighbor)
        return graph
