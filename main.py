from lark import Lark, Transformer
from django.db.models import Q


class DjangoFilterTransformer(Transformer):
    list = list
    comp_operations = {"=": "", ">": "__gt", "<": "__lt", ">=": "__gte", "<=": "__lte"}

    @staticmethod
    def int(n):
        return int(n[0])

    @staticmethod
    def string(s):
        return s[0][1:-1]

    @staticmethod
    def true(_):
        return True

    @staticmethod
    def false(_):
        return False

    @staticmethod
    def DATE(d):
        return str(d)

    @staticmethod
    def not_expr(args):
        return ~args[0]

    @staticmethod
    def in_(args):
        field, value = (2, 0) if isinstance(args[0], list) else (0, 2)
        return Q(**{f"{args[field]}__in": args[value]})

    @staticmethod
    def bool_expr(args):
        left, op, right = args
        if op == "|":
            return left | right
        elif op == "&":
            return left & right
        return args

    def q_expr(self, args):
        if len(args) == 3:
            field, operation, value = args
            if operation in self.comp_operations.keys():
                return Q(**{f"{field}{self.comp_operations[operation]}": value})
            else:
                return self.in_(args)
        return args


with open("grammar.enbf", "r") as file:
    grammar = file.read()

parser = Lark(grammar)
# text = "(assignee=1|[1] in assistants|position=1)&~status in [1,2]"
# text = "assignee in [2,3,4] | [2,3,4] in assistants | position=2"
# text = "(assignee=1|[1] in assistants|position=1)&~(status=3&create_date<=2024-01-15)"
text = "create_date<=2014-01-15"
tree = parser.parse(text=text)
print(tree.pretty())
res = DjangoFilterTransformer().transform(tree)
filter = (Q(assignee=1) | Q(assistants__in=[1]) | Q(position=1)) & ~Q(status__in=[1,2])
print(res)
print(filter)
print(res == filter)
