from src.graph import Graph
from src.parser.line_parser import parse_lines
from src.parser.block_parser import ProgramBlock, BlockType, subdivide_if, subdivide_while


class ProgramParser:
    def __init__(self, source_code: str):
        lines = parse_lines(source_code)
        self.program = ProgramBlock(lines)
        self.graph = Graph()
        self.node_content = {}
        
    def print(self) -> None:
        self.program.print()
        
    def populate_graph(self) -> None:
        self._populate_graph(self.program)
        self.replace_nodes()
    
    @classmethod
    def from_file(cls, path_to_program: str) -> "ProgramParser":
        with open(path_to_program, "r") as f:
            source_code = f.read()
        return cls(source_code)
    
    def _populate_graph(self, block: ProgramBlock) -> None:
        """Recursively populates the graph attribute of the ProgramParser object."""
        
        if block.is_empty():
            return
        
        if block.type == BlockType.WHILE_BLOCK:
            blocks = subdivide_while(block)
            head, body, tail = blocks["head"], blocks["body"], blocks["tail"]
            
            self.graph.add_node(head.id)
            self.graph.add_node(body.id)
            self.graph.add_node(tail.id)
            
            self.graph.add_edge(head.id, body.id)
            self.graph.add_edge(body.id, head.id)
            self.graph.add_edge(body.id, tail.id)
            
            self.node_content[head.id] = head
            self.node_content[body.id] = body
            self.node_content[tail.id] = tail
            
            self._populate_graph(body)
            self._populate_graph(tail)
            
        elif block.type == BlockType.IF_BLOCK:
            blocks = subdivide_if(block)
            head, if_body, else_body, tail = (
                blocks["head"],
                blocks["if_body"],
                blocks["else_body"],
                blocks["tail"],
            )
            
            self.graph.add_node(head.id)
            self.graph.add_node(if_body.id)
            self.graph.add_node(else_body.id)
            self.graph.add_node(tail.id)
            
            self.graph.add_edge(head.id, if_body.id)
            self.graph.add_edge(head.id, else_body.id)
            self.graph.add_edge(if_body.id, tail.id)
            self.graph.add_edge(else_body.id, tail.id)
            
            self.node_content[head.id] = head
            self.node_content[if_body.id] = if_body
            self.node_content[else_body.id] = else_body
            self.node_content[tail.id] = tail
            
            self._populate_graph(if_body)
            self._populate_graph(else_body)
            self._populate_graph(tail)
            
        elif block.type == BlockType.SIMPLE:
            self.graph.add_node(block.id)
            self.node_content[block.id] = block
        else:
            raise ValueError(f"Invalid block type: {block.type}")
        
    def replace_nodes(self) -> None:
        """Replaces the nodes of the graph by their content."""
        for i in range(self.graph.num_nodes):
            node = self.graph.nodes[i]
            self.graph.nodes[i] = self.node_content[node]
        for i in range(self.graph.num_edges):
            source, target = self.graph.edges[i]
            self.graph.edges[i] = (self.node_content[source], self.node_content[target])
        if not self.graph.validate():
            raise ValueError("Invalid graph")
        