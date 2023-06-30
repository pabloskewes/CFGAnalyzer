from typing import List, Dict
from enum import Enum
from copy import deepcopy

from src.parser.line_parser import LineType, Line


def is_control_flow(line: Line) -> bool:
    """
    Returns True if the line is a control flow statement.
    """
    return line.type in [LineType.IF, LineType.ELSE, LineType.WHILE]


class BlockType(Enum):
    EMPTY = "EMPTY"
    SIMPLE = "SIMPLE"
    IF_BLOCK = "IF_BLOCK"
    WHILE_BLOCK = "WHILE_BLOCK"


class ProgramBlock:
    """
    Structure representing a block of code.
    Attributes:
        id: id of the block
        lines: list of lines of the block
    """
    BLOCK_COUNTER = 1

    def __init__(self, lines: List[Line] = []):
        self.lines = deepcopy(lines)
        self._id = ProgramBlock.BLOCK_COUNTER
        ProgramBlock.BLOCK_COUNTER += 1

    @property
    def type(self) -> BlockType:
        return self._determine_block_type()

    @property
    def id(self):
        if self.is_empty():
            return self._id * -1
        return self.lines[0].line_number
    
    def __str__(self) -> str:
        if self.is_empty():
            return f"EMPTY {self._id}"
        return "\n".join(line.content for line in self.lines)

    def __repr__(self):
        return f"ProgramBlock({self.lines=})"
    
    def __eq__(self, other):
        return self.lines == other.lines
    
    def str_block(self) -> str:
        code = ""
        for line in self.lines:
            code += "\t" * line.tabs + line.content + "\n"
        return code
    
    def print(self) -> str:
        code = ""
        for line in self.lines:
            code += "\t" * line.tabs + line.content + "\n"
        print(code)

    def is_empty(self) -> bool:
        return not self.lines

    def add_line(self, line: Line):
        self.lines.append(line)

    def has_same_ident(self) -> bool:
        if self.is_empty():
            return True
        return all(line.tabs == self.lines[0].tabs for line in self.lines)

    def has_control_flow(self) -> bool:
        return any(is_control_flow(line) for line in self.lines)

    def is_simple(self) -> bool:
        if self.is_empty():
            return True
        return not self.has_control_flow() and self.has_same_ident()

    def _determine_block_type(self) -> BlockType:
        if self.is_empty():
            return BlockType.SIMPLE
        for line in self.lines:
            if line.type == LineType.IF:
                return BlockType.IF_BLOCK
            elif line.type == LineType.WHILE:
                return BlockType.WHILE_BLOCK
        return BlockType.SIMPLE


def subdivide_if(block: ProgramBlock) -> Dict[str, "ProgramBlock"]:
    head_block = ProgramBlock()
    if_block = ProgramBlock()
    else_block = ProgramBlock()
    tail_block = ProgramBlock()

    current_ident = block.lines[0].tabs
    for line in block.lines:
        if line.tabs != current_ident:
            raise ValueError("Invalid block")

        head_block.add_line(line)
        if line.type == LineType.IF:
            break

    if_index = len(head_block.lines)
    if_block_ident = current_ident + 1
    for line in block.lines[if_index:]:
        if line.tabs < if_block_ident:
            break
        if_block.add_line(line)


    else_index = len(head_block.lines) + len(if_block.lines)
    if else_index < len(block.lines) and block.lines[else_index].type == LineType.ELSE:
        else_block_ident = current_ident + 1
        for line in block.lines[else_index + 1 :]:
            if line.tabs < else_block_ident:
                break
            else_block.add_line(line)

        tail_index = (
            len(head_block.lines) + len(if_block.lines) + len(else_block.lines) + 1
        )
        tail_block.lines = block.lines[tail_index:]
    else:
        tail_index = len(head_block.lines) + len(if_block.lines)
        tail_block.lines = block.lines[tail_index:]

    return {
        "head": head_block,
        "if_body": if_block,
        "else_body": else_block,
        "tail": tail_block,
    }


def subdivide_while(block: ProgramBlock) -> Dict[str, "ProgramBlock"]:
    head_block = ProgramBlock()
    while_block = ProgramBlock()
    tail_block = ProgramBlock()

    current_ident = block.lines[0].tabs

    for line in block.lines:
        if line.tabs != current_ident:
            raise ValueError("Invalid block")

        head_block.add_line(line)
        if line.type == LineType.WHILE:
            break

    while_index = len(head_block.lines)
    while_block_ident = current_ident + 1

    for line in block.lines[while_index:]:
        if line.tabs < while_block_ident:
            break
        while_block.add_line(line)

    tail_index = len(head_block.lines) + len(while_block.lines)
    tail_block.lines = block.lines[tail_index:]

    return {"head": head_block, "while_body": while_block, "tail": tail_block}
    