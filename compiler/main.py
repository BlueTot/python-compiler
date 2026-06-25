from lark import Lark
from parser import ASTBuilder, CompileError
from semantic import SemanticChecker, SemanticError


"""
Main structure of the compiler:

grammar
parser -> AST
semantic analysis -> correct AST
code generation -> assembly code

"""


parser = Lark.open("./grammar.lark", parser="lalr", transformer=ASTBuilder())


def compile(program: str) -> None:
    """
        Main entry point to the program
        Takes a program as string and performs parsing and semantic analysis
        
        prints "All Ok" if no errors, 
        "SemanticError: ..." if there is a semantic error, or 
        "CompileError: ..." if there is a compile (parsing) error
    """

    try:

        ast = parser.parse(program)
        SemanticChecker().check(ast)
        print("All Ok")

    except CompileError as e:
        print(f"CompileError: {e}")
    except SemanticError as e:
        print(f"SemanticError: {e}")
    


if __name__ == "__main__":
    with open("./code.txt") as f:
        program = f.read()
    compile(program)
