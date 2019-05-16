
from string import ascii_uppercase
from Token import *

class Lexer():

    def __init__(self, text):
        self.text = text
        self.pos = 0
        if text:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def error(self):
        line_count = self.text[:self.pos].count("\n")
        line = self.text.split("\n")[line_count]
        index = line.index(self.current_char)
        arrow = " "*index + "^"
        raise Exception('[-] Invalid character: "{}" at line:{}\n{}\n{}'\
                .format(self.current_char, line_count, line, arrow))

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char is not "\n":
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char is not "\n":
            self.advance()

    def peek(self, num):
        peek_pos = self.pos + num
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]


    def get_next_token(self):

        tokens = {'+': AND, '|': OR, '!': NEG, '^': XOR, '(':LPAREN, ')':RPAREN, "\n":NEWLINE}

        while self.current_char is not None:

            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isspace() and self.current_char is not "\n":
                self.skip_whitespace()
                continue

            if self.current_char in ascii_uppercase:
                ret_value = self.current_char
                self.advance()
                return (Token(FACTOR, ret_value))

            if self.current_char in (key for key in tokens.keys()):
                ret_value = self.current_char
                self.advance()
                return Token(tokens[ret_value], ret_value)

            if self.current_char == '=' and self.peek(1) == '>':
                self.advance()
                self.advance()
                return Token(IMPLIES, '=>')

            if self.current_char == '=':
                self.advance()
                return Token(INIT, '=')

            if self.current_char == '?':
                self.advance()
                return Token(QUERY, '?')

            self.error()
        return Token(EOF, None)
