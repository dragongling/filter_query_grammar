import unittest

from lark import Lark

from main import DjangoFilterTransformer


class TestLarkParser(unittest.TestCase):
    def setUp(self):
        with open("grammar.enbf", "r") as file:
            grammar = file.read()

        self.parser = Lark(grammar, parser="lalr")

    def test1(self):
        text = "assignee=1"
        tree = self.parser.parse(text)
        res = DjangoFilterTransformer().transform(tree)
        self.assertEqual(str(res), "(AND: ('assignee', 1))")

    def test2(self):
        text = "assignee=1|position=1"
        tree = self.parser.parse(text)
        res = DjangoFilterTransformer().transform(tree)
        self.assertEqual(str(res), "(OR: ('assignee', 1), ('position', 1))")