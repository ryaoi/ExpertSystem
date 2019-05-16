import sys
from Token import *
from Ast import *

class NodeVisitor():
    def visit(self, node, result=None):
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, result)

    def generic_visit(self, node, result=None):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def print(self, node):
        method_name = 'print_{}'.format(type(node).__name__)
        printer = getattr(self, method_name, self.generic_print)
        return printer(node)

    def generic_print(self, node, result=None):
        raise Exception('No print_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):

    def __init__(self, parser, verbose):
        self.parser = parser
        self.factors = {}
        self.queries = []
        self.search = []
        self.recursive = 0
        self.verbose = verbose

    def check_factor(self, node, value):
        if node.token.type == FACTOR and node.value == value:
            return True
        elif node.token.type == NEG:
            return self.check_factor(node.expr, value)
        elif node.token.type != FACTOR:
            left = self.check_factor(node.left, value)
            right = self.check_factor(node.right, value)
            if left == True or right == True:
                return True
        else:
            return False

    def search_rules(self, node, value):
        rules = []
        for rule in node.children:
            if isinstance(rule, NoOp):
                continue
            if rule.op.type == IMPLIES:
                if self.check_factor(rule.right, value):
                    rules.append(rule)
        return rules

    def interpret(self):
        try:
            self.tree = self.parser.parse()
            """
            parse() -> creer l'arbre
            """
        except Exception as e:
            print(e)
            sys.exit(1)
        if self.parser.factors == None:
            print("[-] Error : Missing Facts")
            sys.exit(1)
        if self.parser.queries == None:
            print("[-] Error : Missing Queries")
            sys.exit(1)
        self.factors = self.parser.factors
        self.queries = self.parser.queries
        for query in self.queries:
            token = Token(FACTOR, query)
            try:
                result = self.visit_Factor(Factor(token))
                if result is None:
                    result = "Undefined"
                print("{}:{}".format(query, result))
            except Exception as e:
                print("{}:{}".format(query, e))

    def visit_NegOp(self, node, result=None):
        if node.op.type == NEG:
            return not (self.visit(node.expr, result=result))

    @staticmethod
    def handle_or(left, right):
        if left == None and right == None:
            return None
        elif left == None:
            return right
        elif right == None:
            return left
        else:
            return left or right

    @staticmethod
    def handle_xor(left, right):
        if left == None or right == None:
            return None
        else:
            return left ^ right

    def visit_Op(self, node, result=None):
        if node.op.type == AND:
            left = self.visit(node.left, result=result)
            right = self.visit(node.right, result=result)
            if result is not None:
                if left == None and right == None:
                    return None
                if left == None:
                    return right
                if right == None:
                    return left
                return left or right
            else:
                if left == None or right == None:
                    return None
                return left & right
        elif node.op.type == OR:
            if result is not None:
                return None
            else:
                left = self.visit(node.left)
                right = self.visit(node.right)
                return self.handle_or(left, right)
        elif node.op.type == XOR:
            if result is not None:
                return None
            else:
                left = self.visit(node.left)
                right = self.visit(node.right)
                return self.handle_xor(left, right)

    def visit_ImplyOp(self, node, result=None):
        self.recursive += 1
        if node.op.type == IMPLIES:
            left = self.visit(node.left)
            right = self.visit(node.right, result=left)
            self.recursive -= 1
            return right

    def visit_Factor(self, node, result=None):
        """
        Core of backward-chaining:

        backward_chaining(H):
            if H in fact:
                True
            else if H inside the rule:
				if H aready in search history:
					[-] infinite loop!
                for each rule inside rules:
                    results = []
                    for each antecedent inside rule:
                        results += backward_chaining(antecedent)
                    if false and true in results:
                        [-] Rules are corrupted!
                    if true in results:
                        True
                    else if flase in results:
                        false
                    else
                        None
            else:
                False

        """
        if result is not None:
            if len(self.search) > 0:
                if self.search[-1].value == node.token.value:
                    self.search.pop()
                    return result
            return None
        if node.value in self.factors:
            return True
        rules = self.search_rules(self.tree, node.value)
        if len(rules):
            results = []
            for index, rule in enumerate(rules):
                if node not in self.search:
                    self.search.append(node)
                else:
                    raise Exception("inifinite loop")
                if self.verbose:
                    print("{}Rule {}.{}:["\
                            .format("=="*self.recursive, self.recursive, index + 1), end="")
                    self.print(rule)
                    print("]")
                results.append(self.visit(rule))
            if False in results and True in results:
                raise Exception("Rules are not correct")
            if True in results:
                return True
            elif False in results:
                return False
            else:
                return None
        else:
            return False

    def visit_NoOp(self, node):
        pass


    def print_NoOp(self, node):
        pass

    def print_Factor(self, node):
        if node.value and node.value in self.factors:
            print("{} [True]".format(node.value), end="")
        else:
            print("{}".format(node.value), end="")

    def print_ImplyOp(self, node):
        sign = " => "
        print("(", end="")
        self.print(node.left)
        print(sign, end="")
        self.print(node.right)
        print(")", end="")

    def print_Op(self, node):
        if node.op.type == AND:
            sign = " + "
        elif node.op.type == OR:
            sign = " | "
        else:
            sign = " ^ "
        print("(", end="")
        self.print(node.left)
        print(sign, end="")
        self.print(node.right)
        print(")", end="")

    def print_NegOp(self, node):
        print("!(", end="")
        self.print(node.expr)
        print(")", end="")
