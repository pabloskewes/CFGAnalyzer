from typing import List
from enum import Enum
from pprint import pprint

from src.parser.line_parser import (
    is_function_call,
    is_condition,
    is_assignment,
)


class InvalidLineError(ValueError):
    """Raised when a line is invalid."""

    pass


class LineType(Enum):
    ASSING = "ASSIGN"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FUNCTION = "FUNCTION"

    def __repr__(self):
        return f"LineType.{self.value}"


def clean_string(string: str) -> str:
    string = string.replace("    ", "\t").replace("’", "'")
    return string


def get_line_type(line: str) -> LineType:
    """
    Get the type of a line, raise InvalidLineError if the line is invalid.
    The possible types are:
        - LineType.ASSIGN: assignment
        - LineType.IF: if statement
        - LineType.ELSE: else statement
        - LineType.WHILE: while statement
        - LineType.FUNCTION: function call
    Args:
        line: line to get the type of
    Returns:
        LineType of the line
    """
    if is_assignment(line):
        return LineType.ASSING

    elif line.startswith("if "):
        condition = line[3:].strip()
        if not condition.endswith(":"):
            raise InvalidLineError(f'Invalid if condition: "{line}", missing ":"')
        if not is_condition(condition[:-1]):
            raise InvalidLineError(f"Invalid if condition: {line[3:]}")
        return LineType.IF

    elif line.startswith("else"):
        after_else = line[4:].strip()
        if after_else != ":":
            raise InvalidLineError(f'Invalid else statement: "{line}", missing ":"')
        return LineType.ELSE

    elif line.startswith("while "):
        condition = line[6:].strip()
        if not condition.endswith(":"):
            raise InvalidLineError(f'Invalid while condition: "{line}", missing ":"')
        if not is_condition(condition[:-1]):
            raise InvalidLineError(f"Invalid while condition: {line[6:]}")
        return LineType.WHILE

    elif is_function_call(line):
        return LineType.FUNCTION

    else:
        raise InvalidLineError(f"Invalid line: {line}")


class Line:
    """
    Structure representing a line of code.
    Attributes:
        content: content of the line (without indentation)
        line_number: line number in the program
        tabs: number of tabs at the beginning of the line (indentation level)
        type: type of the line, see LineType
    """

    def __init__(self, content: str, line_number: int):
        content = clean_string(content)

        self.content = content.strip()
        self.line_number = line_number
        self.tabs = len(content) - len(content.lstrip("\t"))
        self.type: LineType = get_line_type(self.content)

    def __repr__(self):
        return f"Line({self.content=}, {self.tabs=}, {self.type=})"


def parse_lines(path_to_program: str) -> List[Line]:
    """
    Parse a program and return a list of its lines having their indentation level
    Args:
        path_to_program: path to the program to parse
    Returns:
        list of Line objects
    """
    parsed_lines = []
    with open(path_to_program, "r") as f:
        lines = f.readlines()
    for line_number, line in enumerate([line for line in lines if line.strip() != ""]):
        parsed_lines.append(Line(line, line_number))
    return parsed_lines


if __name__ == "__main__":
    from pathlib import Path

    ROOT = Path(__file__).parent.parent.parent
    program_path = ROOT / "code_examples" / "code_example4.txt"
    assert program_path.exists()

    lines = parse_lines(program_path)

    pprint(lines)
