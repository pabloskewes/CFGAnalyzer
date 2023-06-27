from typing import List
from enum import Enum
from pprint import pprint

from parser.line_parser import (
    is_var,
    is_constant,
    is_function_call,
    is_condition,
    is_expression,
    is_assignment,
)
    

class LineType(Enum):
    ASSING = 'ASSIGN'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    FUNCTION = 'FUNCTION'
    

class Line:
    def __init__(self, content: str, line_number: int):
        self.content = content.strip()
        self.line_number = line_number
        
        content = content.replace('    ', '\t')
        self.tabs = len(content) - len(content.lstrip('\t'))
    
    def __repr__(self):
        return f'Line({self.content=}, {self.tabs=})'
    

def parse_lines(path_to_program: str) -> List[Line]:
    """
    Parse a program and return a list of its lines having their indentation level
    Args:
        path_to_program: path to the program to parse
    Returns:
        list of Line objects
    """
    parsed_lines = []
    with open(path_to_program, 'r') as f:
        lines = f.readlines()
    for line_number, line in enumerate([line for line in lines if line.strip() != '']):
        parsed_lines.append(Line(line, line_number))
    return parsed_lines


# class ProgramParser:
#     def __init__(self) -> None:
#         self.lines: List[Line] = []
        
#     def parse(self, path: str) -> None:
#         self._parse_lines(path=path)
        
#     def _parse_lines(self, path: str) -> None:
#         """Parse a program."""
#         with open(path, 'r') as f:
#             lines = f.readlines()
#         for line_number, line in enumerate(lines):
#             self.lines.append(Line(line, line_number))
        
    
    
    
if __name__ == '__main__':
    from pathlib import Path
    ROOT = Path(__file__).parent.parent.parent
    program_path = ROOT / 'code_examples' / 'code_example4.txt'
    assert program_path.exists()
    
    lines = parse_lines(program_path)
    
    pprint(lines)
    
        
    