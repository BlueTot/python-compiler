from pathlib import Path
from lark import Lark
from lark.exceptions import LarkError
from .parser import ASTBuilder, CompileError
from .semantic import SemanticChecker, SemanticError


"""
Main structure of the compiler:

grammar
parser -> AST
semantic analysis -> correct AST
code generation -> assembly code
"""


GRAMMAR_PATH = Path(__file__).with_name("grammar.lark")

parser = Lark.open(
    str(GRAMMAR_PATH),
    parser="lalr",
    transformer=ASTBuilder(),
)


def compile(program: str) -> None:
    """
    Main compiler entry point used by tests.
    """

    try:
        ast = parser.parse(program)
    except LarkError as e:
        print(e)
        raise CompileError("syntax error") from e

    SemanticChecker().check(ast)


def main() -> None:
    code_path = Path(__file__).with_name("code.txt")

    with open(code_path) as f:
        program = f.read()

    try:
        compile(program)
        print("All Ok")
    except SemanticError as e:
        print(f"SemanticError: {e}")
    except CompileError as e:
        print(f"CompileError: {e}")


if __name__ == "__main__":
    main()