import unittest
from src.parser.line_parser_utils import (
    clean_string,
    is_var,
    is_constant,
    is_string,
    is_function_call,
    is_condition,
    is_expression,
    is_assignment,
)


class LineParserUtilsTestCase(unittest.TestCase):
    def test_clean_string(self):
        self.assertEqual(clean_string("    "), "\t")
        self.assertEqual(clean_string("    if "), "\tif ")
        self.assertEqual(clean_string("’"), "'")
        self.assertFalse(clean_string("    ") == "    ")
        
    def test_is_var(self):
        self.assertTrue(is_var("a"))
        self.assertTrue(is_var("b"))
        self.assertFalse(is_var("A"))
        self.assertFalse(is_var("1"))
        self.assertFalse(is_var("ab"))
        self.assertFalse(is_var("a1"))

    def test_is_constant(self):
        self.assertTrue(is_constant("1"))
        self.assertTrue(is_constant("2"))
        self.assertTrue(is_constant("100"))
        self.assertFalse(is_constant("a"))
        self.assertFalse(is_constant("A"))
        self.assertFalse(is_constant("1a"))

    def test_is_string(self):
        self.assertTrue(is_string('"a"'))
        self.assertTrue(is_string("'a'"))
        self.assertTrue(is_string('"This is a string"'))
        self.assertTrue(is_string("'This is a string (2+2+2)'"))
        self.assertFalse(is_string("a"))
        self.assertFalse(is_string("1"))

    def test_is_function_call(self):
        self.assertTrue(is_function_call("f()"))
        self.assertTrue(is_function_call("f(a)"))
        self.assertTrue(is_function_call("f(a, b)"))
        self.assertTrue(is_function_call("f(a, b + 3)"))
        self.assertTrue(is_function_call('print("hello")'))
        self.assertTrue(is_function_call('print(2 + 3, a*2, "hello")'))
        self.assertFalse(is_function_call("f"))
        self.assertFalse(is_function_call("f(a"))
        self.assertFalse(is_function_call("f(a, b"))

    def test_is_expression(self):
        self.assertTrue(is_expression("a"))
        self.assertTrue(is_expression("a + b"))
        self.assertTrue(is_expression("a + b + c"))
        self.assertTrue(is_expression("f(x, y, z)"))
        self.assertTrue(is_expression("f(a, b) + c"))
        self.assertTrue(is_expression("a + f(a, b)"))
        self.assertTrue(is_expression("22 % 2 + x"))
        self.assertTrue(is_expression("ff(ff(ff(x)))"))
        self.assertTrue(is_expression("ff(ff(ff(x**2)))"))

    def test_is_condition(self):
        self.assertTrue(is_condition("a == b"))
        self.assertTrue(is_condition("a != b"))
        self.assertTrue(is_condition("a**2 < b"))
        self.assertTrue(is_condition("f(x, y) + 4 > b + 2"))
        self.assertTrue(is_condition("a <= f(a, b)"))
        self.assertTrue(is_condition("a >= f(f(x, y), f(x, y))"))
        self.assertFalse(is_condition("a"))

    def test_is_assignment(self):
        self.assertTrue(is_assignment("a = 2"))
        self.assertTrue(is_assignment("a = b"))
        self.assertTrue(is_assignment("a = f(a, b)"))
        self.assertTrue(is_assignment("a = f(a, b) + 2"))
        self.assertTrue(is_assignment("a = f(a, b) + f(a, b)"))
        self.assertFalse(is_assignment("a"))
        self.assertFalse(is_assignment("a + 2"))
        self.assertFalse(is_assignment("a + 2 = b"))
