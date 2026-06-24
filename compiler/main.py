from lark import Lark
from parser import ASTBuilder


"""
Main structure of the compiler:

grammar
parser -> AST
semantic analysis -> correct AST
code generation -> assembly code

"""


parser = Lark.open("./grammar.lark", parser="lalr", transformer=ASTBuilder())


def main() -> None:
    with open("./code.txt") as f:
        program = f.read()
    print(parser.parse(program))

if __name__ == "__main__":
    main()