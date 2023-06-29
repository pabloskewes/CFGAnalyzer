import unittest

from pathlib import Path
from src.parser.block_parser import (
    ProgramBlock,
    BlockType,
    subdivide_if,
    subdivide_while,
)
from src.parser.line_parser import LineType, parse_lines


EXAMPLES_PATH = Path(__file__).parent.parent / "code_examples"


class ProgramBlockTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """
        Tests the following program:
        x = 0
        while x < 10:
            if x > 5:
                print(x)
            else:
                print('x es menor que 6')
            x = x + 1
        """
        super(ProgramBlockTest, self).__init__(*args, **kwargs)
        program_path = EXAMPLES_PATH / "code_example5.txt"
        self.lines = parse_lines(program_path.read_text())

    def test_is_empty(self):
        block = ProgramBlock()
        self.assertTrue(block.is_empty())
        block = ProgramBlock(self.lines)
        self.assertFalse(block.is_empty())

    def test_has_same_ident(self):
        block = ProgramBlock(self.lines)
        self.assertFalse(block.has_same_ident())
        block = ProgramBlock(self.lines[:2])
        self.assertTrue(block.has_same_ident())

    def test_has_control_flow(self):
        block = ProgramBlock(self.lines)
        self.assertTrue(block.has_control_flow())
        block = ProgramBlock(self.lines[0:1])
        self.assertFalse(block.has_control_flow())

    def test_is_simple(self):
        block = ProgramBlock(self.lines)
        self.assertFalse(block.is_simple())
        block = ProgramBlock(self.lines[0:1])
        self.assertTrue(block.is_simple())

    def test_determine_block_type(self):
        block = ProgramBlock(self.lines)
        self.assertEqual(block.type, BlockType.WHILE_BLOCK)
        block = ProgramBlock(self.lines[2:6])
        self.assertEqual(block.type, BlockType.IF_BLOCK)


class ProgramBlockDivisionTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """
        Tests the following program:
        x = 0
        while x > 5:
            y = 3
            if y < 10:
                y = y + 1

        if z == 5:
            print("z is 5")
        else:
            while z < 10:
                print("z is less than 10")
        """
        super(ProgramBlockDivisionTest, self).__init__(*args, **kwargs)
        program_path = EXAMPLES_PATH / "code_example10.txt"
        self.lines = parse_lines(program_path.read_text())

    def test_divide(self):
        block = ProgramBlock(self.lines)
        sub_blocks = subdivide_while(block)
        head, body, tail = (
            sub_blocks["head"],
            sub_blocks["while_body"],
            sub_blocks["tail"],
        )

        self.assertEqual(head.type, BlockType.WHILE_BLOCK)
        self.assertTrue(head.has_control_flow())
        self.assertTrue(head.has_same_ident())
        self.assertEqual(head.lines[-1].type, LineType.WHILE)
        self.assertEqual(head.lines[-1].content, "while x > 5:")

        self.assertEqual(body.lines, self.lines[2:5])
        self.assertEqual(tail.type, BlockType.IF_BLOCK)

        sub_blocks = subdivide_if(body)
        sub_head, sub_if_body, sub_else_body, sub_tail = (
            sub_blocks["head"],
            sub_blocks["if_body"],
            sub_blocks["else_body"],
            sub_blocks["tail"],
        )

        self.assertEqual(sub_head.lines, self.lines[2:4])
        self.assertEqual(sub_if_body.lines, self.lines[4:5])
        self.assertEqual(sub_else_body.lines, [])
        self.assertEqual(sub_tail.lines, [])

        sub_blocks = subdivide_if(tail)
        sub_head, sub_if_body, sub_else_body, sub_tail = (
            sub_blocks["head"],
            sub_blocks["if_body"],
            sub_blocks["else_body"],
            sub_blocks["tail"],
        )

        self.assertEqual(sub_head.lines, self.lines[5:6])
        self.assertEqual(sub_if_body.lines, self.lines[6:7])
        self.assertEqual(sub_else_body.lines, self.lines[8:10])
        self.assertEqual(sub_tail.lines, [])
