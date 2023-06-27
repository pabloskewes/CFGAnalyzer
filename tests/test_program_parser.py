import unittest
from pathlib import Path

from src.parser.program_parser import (
    clean_string,
    get_line_type,
    parse_lines,
    LineType,
    InvalidLineError,
)


class TestLineParser(unittest.TestCase):
    def test_clean_string(self):
        self.assertEqual(clean_string("    "), "\t")
        self.assertEqual(clean_string("    if "), "\tif ")
        self.assertEqual(clean_string("’"), "'")
        self.assertFalse(clean_string("    ") == "    ")

    def test_get_line_type(self):
        self.assertEqual(get_line_type("a = 1"), LineType.ASSING)
        self.assertEqual(get_line_type("if a == 1:"), LineType.IF)
        self.assertEqual(get_line_type("else:"), LineType.ELSE)
        self.assertEqual(get_line_type("while a == 1:"), LineType.WHILE)
        self.assertEqual(get_line_type("print(a)"), LineType.FUNCTION)

        with self.assertRaises(InvalidLineError):
            get_line_type("a = 1 +")
        with self.assertRaises(InvalidLineError):
            get_line_type("if a == 1")
        with self.assertRaises(InvalidLineError):
            get_line_type("else")
        with self.assertRaises(InvalidLineError):
            get_line_type("while a == 1")
        with self.assertRaises(InvalidLineError):
            get_line_type("print(a")

    def test_parse_lines(self):
        """
        Tests the following program:
        x = 0
        while x < 10:
            if x > 5:
                print(x)
            else :
                print( ’x es menor que 6’)

            x = x + 1
        """
        ROOT = Path(__file__).parent.parent
        program_path = ROOT / "code_examples" / "code_example4.txt"
        self.assertTrue(program_path.exists())

        lines = parse_lines(program_path)

        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0].content, "x = 0")
        self.assertEqual(lines[0].line_number, 0)
        self.assertEqual(lines[0].tabs, 0)
        self.assertEqual(lines[0].type, LineType.ASSING)
        self.assertEqual(lines[1].content, "while x < 10:")
        self.assertEqual(lines[1].line_number, 1)
        self.assertEqual(lines[1].tabs, 0)
        self.assertEqual(lines[1].type, LineType.WHILE)
        self.assertEqual(lines[2].content, "if x > 5:")
        self.assertEqual(lines[2].line_number, 2)
        self.assertEqual(lines[2].tabs, 1)
        self.assertEqual(lines[2].type, LineType.IF)
        self.assertEqual(lines[3].content, "print(x)")
        self.assertEqual(lines[3].line_number, 3)
        self.assertEqual(lines[3].tabs, 2)
        self.assertEqual(lines[3].type, LineType.FUNCTION)
        self.assertEqual(lines[4].content, "else :")
        self.assertEqual(lines[4].line_number, 4)
        self.assertEqual(lines[4].tabs, 1)
        self.assertEqual(lines[4].type, LineType.ELSE)
        self.assertEqual(lines[5].content, "print( 'x es menor que 6')")
        self.assertEqual(lines[5].line_number, 5)
        self.assertEqual(lines[5].tabs, 2)
        self.assertEqual(lines[5].type, LineType.FUNCTION)
        self.assertEqual(lines[6].content, "x = x + 1")
        self.assertEqual(lines[6].line_number, 6)
        self.assertEqual(lines[6].tabs, 1)
        self.assertEqual(lines[6].type, LineType.ASSING)
