
class Ast():
    pass

class Rule(Ast):
    def __init__(self):
        self.children = []

class NoOp(Ast):
    pass

class NegOp(Ast):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Op(Ast):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class ImplyOp(Ast):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Factor(Ast):
    def __init__(self, token):
        self.token = token
        self.value = token.value
