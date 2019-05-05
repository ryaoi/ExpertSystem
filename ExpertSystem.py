
import sys
import argparse
from Lexer import Lexer
from Interpreter import Interpreter
from Parser import Parser

def ExpertSystem(inputFile, verbose):
    try:
        with open(inputFile) as f:
            content = f.readlines()
    except Exception as e:
        print("{}".format(e))
        sys.exit(1)
    lexer = Lexer("".join(content))
    parser = Parser(lexer)
    interpreter = Interpreter(parser, verbose)
    interpreter.interpret()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", \
					help="increase output verbosity", action="store_true")
    parser.add_argument("input_file")
    args = parser.parse_args()
    ExpertSystem(args.input_file, args.verbose)
