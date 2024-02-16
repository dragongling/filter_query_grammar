from lark import Lark, Transformer
from django.db.models import Q


class DjangoFilterTransformer(Transformer):
    list = list
    comp_operations = {"=": "", ">": "__gt", "<": "__lt", ">=": "__gte", "<=": "__lte"}

    def int(self, n):
        return int(n[0])

    def string(self, s):
        return s[0][1:-1]

    def true(self, _):
        return True

    def false(self, _):
        return False

    def date(self, d):
        return d[0]

    def field(self, f):
        return f[0]

    def value(self, v):
        return v[0]

    def not_expr(self, args):
        return ~args[0]

    def in_(self, args):
        if isinstance(args[0], list):  
            return Q(**{f"{args[2]}__in": args[0]})
        else:  
            return Q(**{f"{args[0]}__in": args[2]})

    def expr(self, args):
        if len(args) == 1:
            return args[0]
        elif len(args) == 3:
            left, op, right = args
            if isinstance(op, str):
                if op == "|":
                    return left | right
                elif op == "&":
                    return left & right
        return args

    def q_expr(self, args):
        if len(args) == 3:
            field, operation, value = args
            if isinstance(operation, str) and operation in self.comp_operations.keys():
                return Q(**{f"{field}{self.comp_operations[operation]}": value})
            else:
                return self.in_(args)
        return args

    def start(self, args):
        return args[0]


with open("grammar.enbf", "r") as file:
    grammar = file.read()

parser = Lark(grammar, parser="lalr")
text = "(assignee=1|[1] in assistants|position=1)&~status=3"

tree = parser.parse(text=text)
print(tree.pretty())
res = DjangoFilterTransformer().transform(tree)
filter = (Q(assignee=1) | Q(assistants__in=[1]) | Q(position=1)) & ~Q(status=3)
print(res)
print(filter)
print(res == filter)
