import unittest
import requests
from utils import text_concat, check_dtype


class TestUtils(unittest.TestCase):

    def test_text_concat(self):
        self.assertEqual(text_concat([""], "<foo>", "</foo>"), "<foo></foo>")
        self.assertEqual(text_concat(["A"], "<foo>", "</foo>"), "<foo>A</foo>")
        self.assertEqual(text_concat(["A", "B"], "<foo>", "</foo>"),
                         "<foo>A</foo>, and <foo>B</foo>")
        self.assertEqual(text_concat(["A", "B", "C"], "<foo>", "</foo>"),
                         "<foo>A</foo>, <foo>B</foo>, and <foo>C</foo>")

    def test_check_dtype(self):
        self.assertEqual(
            check_dtype(
                ("dog", int(1), [
                    "a", "b", "c"]), [
                    "str", "int", "list"])[0], True)
