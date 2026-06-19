from lark import Lark, Transformer, v_args
from dataclasses import dataclass

    

@dataclass
class Block:
    statements: list[int]

@dataclass
class Assignment:
    var_name: str
    value: Expression

@dataclass
class IfStatement:
    condition: Condition 
    true_branch: Block
    false_branch: Block | None








@v_args(inline=True)
class ASTBuilder(Transformer):

    """
        builds the AST
    """

    def block(self, *statements) -> None:
        pass

    def assignment(self, var_name, var_expression) -> None:
        pass

    def if_statement(self, condition, if_block) -> None:
        pass

    def while_statement(self, condition, loop_block) -> None:
        pass

    def for_statement(self, initial, condition, increment, loop_block) -> None:
        pass

    def greater_than(self, expr1, expr2) -> None:
        pass

    def less_than(self, expr1, expr2) -> None:
        pass

    def not_equal_to(self, expr1, expr2) -> None:
        pass

    def greater_than_equal(self, expr1, expr2) -> None:
        pass

    def less_than_equal(self, expr1, expr2) -> None:
        pass

    def add(self, expr1, expr2) -> None:
        pass

    def sub(self, expr1, expr2) -> None:
        pass

    def mul(self, expr1, expr2) -> None:
        pass

    def mul(self, expr1, expr2) -> None:
        pass

    def div(self, expr1, expr2) -> None:
        pass

    def number(self, value) -> None:
        pass

    def neg(self, expr) -> None:
        pass

    def var(self, name) -> None:
        pass



parser = Lark.open("./grammar.lark", parser="lalr", transformer=ASTBuilder())


def main() -> None:
    with open("./code.txt") as f:
        program = f.read()
    print(parser.parse(program))

if __name__ == "__main__":
    main()