from lark import Lark, Transformer, v_args
from dataclasses import dataclass

    
"""
Dataclasses for AST nodes
"""


@dataclass
class Expression:
    pass

@dataclass
class AddExpression(Expression):
    expr1: Expression
    expr2: Expression

@dataclass
class SubExpression(Expression):
    expr1: Expression
    expr2: Expression

@dataclass
class MulExpression(Expression):
    expr1: Expression
    expr2: Expression

@dataclass
class DivExpression(Expression):
    expr1: Expression
    expr2: Expression

@dataclass
class NegatedExpression(Expression):
    expr: Expression

@dataclass
class Number(Expression):
    value: int

@dataclass
class Variable(Expression):
    name: str

@dataclass
class Condition:
    pass

@dataclass
class GreaterThanCondition:
    expr1: Expression
    expr2: Expression

@dataclass
class LessThanCondition:
    expr1: Expression
    expr2: Expression

@dataclass
class EqualsCondition:
    expr1: Expression
    expr2: Expression

@dataclass
class NotEqualsCondition:
    expr1: Expression
    expr2: Expression

@dataclass
class GreaterThanOrEqualCondition:
    expr1: Expression
    expr2: Expression

@dataclass
class LessThanOrEqualCondition:
    expr1: Expression
    expr2: Expression

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

@dataclass
class WhileStatement:
    condition: Condition
    loop_body: Block

@dataclass
class ForStatement:
    initial: Assignment
    condition: Condition
    increment: Assignment
    loop_body: Block


"""
AST parser class
"""


@v_args(inline=True)
class ASTBuilder(Transformer):

    """
        builds the AST
    """

    def block(self, *statements) -> Block:
        return Block(list(statements))

    def assignment(self, var_name, var_expression) -> Assignment:
        return Assignment(var_name, var_expression)

    def if_only_statement(self, condition, if_block) -> IfStatement:
        return IfStatement(condition, if_block, None)

    def if_and_else_statement(self, condition, if_block, else_block) -> IfStatement:
        return IfStatement(condition, if_block, else_block)

    def while_statement(self, condition, loop_block) -> WhileStatement:
        return WhileStatement(condition, loop_block)

    def for_statement(self, initial, condition, increment, loop_block) -> ForStatement:
        return ForStatement(initial, condition, increment, loop_block)

    def greater_than(self, expr1, expr2) -> Condition:
        return GreaterThanCondition(expr1, expr2)

    def less_than(self, expr1, expr2) -> Condition:
        return LessThanCondition(expr1, expr2)

    def not_equal_to(self, expr1, expr2) -> Condition:
        return NotEqualsCondition(expr1, expr2)

    def equal_to(self, expr1, expr2) -> Condition:
        return EqualsCondition(expr1, expr2)

    def greater_than_equal(self, expr1, expr2) -> Condition:
        return GreaterThanOrEqualCondition(expr1, expr2)

    def less_than_equal(self, expr1, expr2) -> Condition:
        return LessThanOrEqualCondition(expr1, expr2)

    def add(self, expr1, expr2) -> Expression:
        return AddExpression(expr1, expr2)

    def sub(self, expr1, expr2) -> Expression:
        return SubExpression(expr1, expr2)

    def mul(self, expr1, expr2) -> Expression:
        return MulExpression(expr1, expr2)

    def div(self, expr1, expr2) -> Expression:
        return DivExpression(expr1, expr2)

    def number(self, value) -> Number:
        return Number(value)

    def neg(self, expr) -> Expression:
        return NegatedExpression(expr)

    def var(self, name) -> Variable:
        return Variable(name)



parser = Lark.open("./grammar.lark", parser="lalr", transformer=ASTBuilder())


def main() -> None:
    with open("./code.txt") as f:
        program = f.read()
    print(parser.parse(program))

if __name__ == "__main__":
    main()