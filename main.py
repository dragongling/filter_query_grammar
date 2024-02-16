from lark import Lark, Transformer
from django.db.models import Q


class DjangoFilterTransformer(Transformer):
    @staticmethod
    def list(items):
        return list(items)

    @staticmethod
    def int(n):
        (n,) = n
        return int(n)

    @staticmethod
    def string(s):
        (s,) = s
        return s[1:-1]

    @staticmethod
    def true(b):
        return True

    @staticmethod
    def false(b):
        return False


class DjangoFilterTransformer2(Transformer):
    list = list

    def int(self, n):
        return int(n[0])

    def string(self, s):
        # Remove the surrounding quotes from the string
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

    def not_op(self, args):
        # Negate the Q object
        return "~"

    def in_(self, args):
        # Handles the 'in' operation, expecting field and list or list and field
        if isinstance(args[0], list):  # list in field scenario
            return Q(**{f"{args[2]}__in": args[0]})
        else:  # field in list scenario
            return Q(**{f"{args[0]}__in": args[2]})

    def or_op(self, v):
        return "|"

    def and_op(self, v):
        return "&"

    def bool_op(self, args):
        op = args[0]
        if op == "or":
            return "|"
        elif op == "and":
            return "&"
        else:
            raise ValueError("Unknown boolean operation")

    def expr(self, args):
        # If it's a simple expression, return as is. For complex expressions, apply boolean logic.
        if len(args) == 1:
            return args[0]
        if len(args) == 2 and args[0] == "~":
            return ~args[1]
        elif len(args) == 3:
            left, op, right = args
            if isinstance(op, str):  # Boolean operation
                if op == "|":
                    return left | right
                elif op == "&":
                    return left & right
        return args

    def q_expr(self, args):
        # Handles comparison and in operations
        if len(args) == 3:
            field, operation, value = args
            if isinstance(operation, str) and operation in ["=", ">", "<", ">=", "<="]:
                # Map grammar symbols to Django query keywords
                operation_map = {"=": "", ">": "__gt", "<": "__lt", ">=": "__gte", "<=": "__lte"}
                return Q(**{f"{field}{operation_map[operation]}": value})
            else:
                # For 'in' operation handled separately
                return self.in_(args)
        return args

    # Handling comparison operators directly to return the operator symbol
    def eq(self, _):
        return "="

    def gt(self, _):
        return ">"

    def lt(self, _):
        return "<"

    def gte(self, _):
        return ">="

    def lte(self, _):
        return "<="

    def start(self, args):
        # The starting point of the transformation, should return the fully formed Q object
        return args[0]


with open("grammar.enbf", "r") as file:
    grammar = file.read()

parser = Lark(grammar, parser="lalr")
text = "(assignee>=1|[1] in assistants|position=1)&~status=3"
# text = "~assignee=1"
tree = parser.parse(text=text)
print(tree.pretty())
res = DjangoFilterTransformer2().transform(tree)
# filter = (Q(assignee=1) | Q(assistants__in=[1]) | Q(position=1)) & ~Q(status=3)
print(res)
