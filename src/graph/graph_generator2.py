from typing import List

from src.parser.program_parser import parse_lines, LineType, Line
from src.graph import Graph


def is_control_flow(line: Line) -> bool:
    """
    Returns True if the line is a control flow statement.
    """
    return line.type in [LineType.IF, LineType.ELSE, LineType.WHILE]


class InvalidBlockError(ValueError):
    """Raised when a block is invalid."""
    pass
    

class Block:
    """
    Structure representing a block of code.
    Attributes:
        id: id of the block
        lines: list of lines of the block
    """
    def __init__(self, lines: List[Line] = []):
        self.lines = lines
        
    def add_line(self, line: Line):
        self.lines.append(line)
        
    def is_simple(self) -> bool:
        """
        Returns True if the block is simple, i.e. doen't contain any control flow statement.
        """
        return not any(is_control_flow(line) for line in self.lines)
    
    @property
    def id(self):
        return self.lines[0].line_number
    
    
def get_id(lines: List[Line]) -> int:
    return lines[0].line_number
        
        
class ControlFlowGraph:
    def __init__(self, path: str):
        self.lines = parse_lines(path)
        self.graph = Graph()
        self.node_content = {}
        
        self.populate_graph(Block(self.lines))

        
    def populate_graph(self, block: Block):
        print(f"We are in block {block.id}")
        if not block.lines:
            return
        
        head_lines = []
        ident_level = block.lines[0].tabs
        
        for i in range(len(block.lines)):
            line = block.lines[i]
            if line.tabs == ident_level:
                head_lines.append(line)
                if line.type == LineType.WHILE:
                    header = Block(head_lines)
                    self.node_content[header.id] = header
                    self.graph.add_node(header.id)
                    body_index = i + 1
                    for j in range(i + 1, len(block.lines)):
                        if block.lines[j].tabs == ident_level + 1:
                            body_index = j
                        else:
                            break
                        
                    body = Block(block.lines[i + 1:body_index + 1])
                    outside_while = Block(block.lines[body_index + 1:])
                    self.node_content[body.id] = body
                    self.node_content[outside_while.id] = outside_while
                    
                    self.graph.add_edge(header.id, body.id)
                    self.graph.add_edge(body.id, header.id)
                    self.graph.add_edge(header.id, outside_while.id)
                    
                    self.populate_graph(body)
                    self.populate_graph(outside_while)
                    
                elif line.type == LineType.IF:
                    header = Block(head_lines)
                    self.node_content[header.id] = header
                    self.graph.add_node(header.id)
                    body_if_index = i + 1
                    body_else_index = i + 1
                    for j in range(i + 1, len(block.lines)):
                        if block.lines[j].tabs == ident_level + 1:
                            body_if_index = j
                        else:
                            break
                    for j in range(body_if_index + 1, len(block.lines)):
                        if block.lines[j].tabs == ident_level + 1:
                            body_else_index = j
                        else:
                            break
                    
                    body_if = Block(block.lines[i + 1:body_if_index + 1])
                    body_else = Block(block.lines[body_if_index + 1:body_else_index + 1])
                    outside_if = Block(block.lines[body_else_index + 1:])
                    
                    self.node_content[body_if.id] = body_if
                    self.node_content[body_else.id] = body_else
                    self.node_content[outside_if.id] = outside_if
                    
                    self.graph.add_edge(header.id, body_if.id)
                    self.graph.add_edge(header.id, body_else.id)
                    self.graph.add_edge(body_if.id, outside_if.id)
                    self.graph.add_edge(body_else.id, outside_if.id)
                    
                    self.populate_graph(body_if)
                    self.populate_graph(body_else)
                    self.populate_graph(outside_if)
                    
                    
        
def generate_graph(
    path: str,
    current    
) -> Graph:
    """
    Takes a path to a program and returns the corresponding graph.

    """
    
    lines = parse_lines(path)
    graph = Graph()
    
    block_lines = []
    block_id = 0
    current_indentation = 0
    for prev_line, next_line in zip(lines, lines[1:]):
        if prev_line.tabs == next_line.tabs:
            block_lines.append(prev_line)
            if is_control_flow(prev_line):
                block = Block(block_lines)
                block.id = block_id
                graph.add_node(block)
                block_lines = []
                block_id += 1
        elif prev_line.tabs < next_line.tabs:
        # if the indentation level increases, we are in a new block
            block_lines.append(prev_line)
        elif prev_line.tabs > next_line.tabs:
            # if the indentation level decreases, we are at the end of a block
            block_lines.append(prev_line)
            block = Block(block_lines)
            block.id = block_id
            graph.add_node(block)
        