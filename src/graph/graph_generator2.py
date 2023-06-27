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
        self.id = None
        self.lines = lines
        
    def add_line(self, line: Line):
        self.lines.append(line)
        
        
def generate_graph(path: str) -> Graph:
    """
    Takes a path to a program and returns the corresponding graph.
    A node corresponds to a block of code. A block of code is a sequence of lines
    with the same indentation level. If a block of code ends with an if/else/while
    statement, the block ends there and the rest of the code is not part of the block but
    a part of a new node of the graph that will contain blocks of code representing the
    flow of the program.
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
        