from lark import Lark
from parser import ASTBuilder
from semantic import SemanticChecker


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

    ast = parser.parse(program)
    # print(ast)

    SemanticChecker().check(ast)
    

if __name__ == "__main__":
    main()