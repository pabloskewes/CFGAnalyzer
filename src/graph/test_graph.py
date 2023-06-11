import unittest
from graph import Graph


class GraphTestCase(unittest.TestCase):
    def test_adjacency_list(self):
        # Create a graph
        graph = Graph()

        # Add nodes
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)

        # Add edges
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(4, 1)

        # Expected adjacency list
        expected_adj_list = {
            1: [2],
            2: [3],
            3: [4],
            4: [1]
        }

        # Test adjacency list
        adj_list = graph.adjacency_list
        self.assertEqual(adj_list, expected_adj_list)

    def test_adjacency_matrix(self):
        # Create a graph
        graph = Graph()

        # Add nodes
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)

        # Add edges
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(4, 1)

        # Expected adjacency matrix
        expected_adj_matrix = [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 0]
        ]

        # Test adjacency matrix
        adj_matrix = graph.adjacency_matrix
        self.assertEqual(adj_matrix, expected_adj_matrix)

    def test_from_nodes_and_edges(self):
        # Create nodes and edges
        nodes = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]

        # Create a graph from nodes and edges
        graph = Graph.from_nodes_and_edges(nodes, edges)

        # Expected adjacency list
        expected_adj_list = {
            1: [2],
            2: [3],
            3: [4],
            4: [1]
        }

        # Test adjacency list
        adj_list = graph.adjacency_list
        self.assertEqual(adj_list, expected_adj_list)

    def test_from_adjacency_list(self):
        # Create an adjacency list
        adj_list = {
            1: [2],
            2: [3],
            3: [4],
            4: [1]
        }

        # Create a graph from adjacency list
        graph = Graph.from_adjacency_list(adj_list)

        # Expected nodes and edges
        expected_nodes = [1, 2, 3, 4]
        expected_edges = [(1, 2), (2, 3), (3, 4), (4, 1)]

        # Test nodes and edges
        self.assertEqual(graph.nodes, expected_nodes)
        self.assertEqual(graph.edges, expected_edges)

    def test_from_adjacency_matrix(self):
        # Create an adjacency matrix
        adj_matrix = [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 0]
        ]

        # Create a graph from adjacency matrix
        graph = Graph.from_adjacency_matrix(adj_matrix)

        # Expected nodes and edges
        expected_nodes = [0, 1, 2, 3]
        expected_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

        # Test nodes and edges
        self.assertEqual(graph.nodes, expected_nodes)
        self.assertEqual(graph.edges, expected_edges)
        
    def test_num_nodes(self):
        # Create a graph
        graph = Graph()

        # Add nodes
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)

        # Test number of nodes
        self.assertEqual(graph.num_nodes, 4)
    
    def test_num_edges(self):
        # Create a graph
        graph = Graph()

        # Add nodes
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)

        # Add edges
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(4, 1)

        # Test number of edges
        self.assertEqual(graph.num_edges, 4)


if __name__ == '__main__':
    unittest.main()
