
FACTOR, AND, OR, XOR, NEG, LPAREN, RPAREN, EOF, IMPLIES, COMMENT, INIT, QUERY, NEWLINE = (
    'FACTOR', 'AND', 'OR', 'XOR', 'NEG', 'LPAREN', 'RPAREN',
    'EOF', 'IMPLIES', 'COMMENT', 'INIT', 'QUERY', 'NEWLINE',
)

class Token():

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type} {value})'\
                .format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()
