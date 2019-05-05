
from Token import *
from Ast import *

class Parser():

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.factors = None
        self.queries = None
    
    def error(self):
        line_count = self.lexer.text[:self.lexer.pos - 1].count("\n")
        lines = self.lexer.text.split("\n")
        count = 0
        index = 0
        for i, line in enumerate(lines):
            if i == line_count:
                while count != self.lexer.pos:
                    count += 1
                    index += 1
            else:
                count += len(line) + 1
        line = lines[line_count]
        arrow = " "*(index - 1) + "^"
        raise Exception('[-] Invalid syntax {} at line:{}\n{}\n{}'\
                .format(self.current_token, line_count + 1, line, arrow))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse(self):
        node = self.rule_statement()
        if self.current_token.type != EOF:
            self.error()
        return node

    def rule_statement(self):
        nodes = self.statement_list()

        root = Rule()
        for node in nodes:
            root.children.append(node)
        return root

    def factor(self):
        """
        factor = FACTOR
                | NEG factor
                | LPAREN expr RPAREN
        """

        token = self.current_token
        if token.type == FACTOR:
            self.eat(FACTOR)
            return Factor(token)
        elif token.type == NEG:
            self.eat(NEG)
            node = NegOp(token, self.factor())
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            self.error()

    def expr(self):
        """
        expr: factor((AND | XOR | OR)factor)*
        """
        node = self.factor()

        while self.current_token.type in (AND, XOR, OR):
            token = self.current_token
            if token.type == AND:
                self.eat(AND)
            elif token.type == XOR:
                self.eat(XOR)
            elif token.type == OR:
                self.eat(OR)

            node = Op(left=node, op=token, right=self.factor())
        return node

    def rule(self):
        """
        rule: expr IMPLIES expr
        """

        node = self.expr()
        token = self.current_token
        if token.type == IMPLIES:
            self.eat(IMPLIES)
        else:
            self.error()
        node = ImplyOp(left=node, op=token, right=self.expr())
        return node

    def statement(self):
        """
        statement: rule
                    | INIT (FACTOR)*
                    | QUERY (FACTOR)*
        """

        if self.current_token.type == INIT:
            self.eat(INIT)
            self.factors = {}
            while self.current_token.type == FACTOR:
                self.factors[self.current_token.value] = True
                self.eat(FACTOR)
            node = NoOp()
        elif self.current_token.type == QUERY:
            self.eat(QUERY)
            self.queries = []
            while self.current_token.type == FACTOR:
                self.queries.append(self.current_token.value)
                self.eat(FACTOR)
            node = NoOp()
        else:
            node = self.rule()
        return node

    def statement_list(self):
        """
        statement_list: (NEWLINE)* statement
                        | statement NEWLINE statement_list
        """
        while self.current_token.type == NEWLINE:
            self.eat(NEWLINE)

        node = self.statement()
        
        results = [node]

        while self.current_token.type == NEWLINE:
            while self.current_token.type == NEWLINE:
                self.eat(NEWLINE)
            if self.current_token.type != EOF:
                results.append(self.statement())
        return results
