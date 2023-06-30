from src.graph import Graph
from src.parser.line_parser import parse_lines
from src.parser.block_parser import ProgramBlock, BlockType, subdivide_if, subdivide_while


class ProgramParser:
    def __init__(self, source_code: str):
        lines = parse_lines(source_code)
        self.source_code = source_code
        self.program = ProgramBlock(lines)
        self.graph = Graph()
        self.last_node = None
        self.node_content = {}
        
    def print(self) -> None:
        self.program.print()
        
    def populate_graph(self) -> None:
        last_node = self._populate_graph(self.program)
        self.last_node = last_node
        # self.replace_nodes()
        
    def add_node(self, node: ProgramBlock) -> None:
        self.graph.add_node(node.id)
        self.node_content[node.id] = node
        
    def add_edge(self, source: ProgramBlock, target: ProgramBlock) -> None:
        self.graph.add_edge(source.id, target.id)
    
    @classmethod
    def from_file(cls, path_to_program: str) -> "ProgramParser":
        with open(path_to_program, "r") as f:
            source_code = f.read()
        return cls(source_code)
    
    def _populate_graph(self, block: ProgramBlock) -> None:
        """Recursively populates the graph attribute of the ProgramParser object."""
        
        if block.type == BlockType.WHILE_BLOCK:
            blocks = subdivide_while(block)
            head, body, tail = blocks["head"], blocks["while_body"], blocks["tail"]
            
            self.add_node(head)
            self.add_node(body)
            
            self.add_edge(head, body)
                       
            end_body = self._populate_graph(body)
            self.add_edge(end_body, head)
            
            self.add_node(tail)
            self.add_edge(head, tail)
            return self._populate_graph(tail)
            
        elif block.type == BlockType.IF_BLOCK:
            blocks = subdivide_if(block)
            head, if_body, else_body, tail = (
                blocks["head"],
                blocks["if_body"],
                blocks["else_body"],
                blocks["tail"],
            )
            
            self.add_node(head)
            self.add_node(if_body)
            self.add_node(else_body)
            
            self.add_edge(head, if_body)
            self.add_edge(head, else_body)
            
            end_if = self._populate_graph(if_body)
            end_else = self._populate_graph(else_body)
            
            self.add_edge(end_if, tail)
            self.add_edge(end_else, tail)
            
            self.add_node(tail)
            return self._populate_graph(tail)
            
        elif block.type == BlockType.SIMPLE:
            self.add_node(block)
            return block
        else:
            raise ValueError(f"Invalid block type: {block.type}")
        
    # def replace_nodes(self) -> None:
    #     """Replaces the nodes of the graph by their content."""
    #     for i in range(self.graph.num_nodes):
    #         node = self.graph.nodes[i]
    #         self.graph.nodes[i] = str(self.node_content[node])
    #     for i in range(self.graph.num_edges):
    #         source, target = self.graph.edges[i]
    #         self.graph.edges[i] = (
    #             str(self.node_content[source]),
    #             str(self.node_content[target]),
    #         )
    #     if not self.graph.validate():
    #         raise ValueError("Invalid graph")
    
    def replace_nodes(self) -> None:
        graph = Graph()
        for node in self.graph.nodes:
            graph.add_node(str(self.node_content[node]))
            
        for source, target in self.graph.edges:
            graph.add_edge(str(self.node_content[source]), str(self.node_content[target]))
            
        self.graph = graph
        self.last_node = str(self.last_node)
        
        
    def plot_cfg(self) -> None:
        self.graph.plot()
        