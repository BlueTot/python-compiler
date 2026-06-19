from lark import Lark, Transformer, v_args
from dataclasses import dataclass
from enum import Enum

    
"""
Dataclasses for AST nodes
"""

# arithemtic expression
@dataclass
class Expression:
    pass

# addition of two expressions
@dataclass
class AddExpression(Expression):
    expr1: Expression
    expr2: Expression

# subtraction of two expressions
@dataclass
class SubExpression(Expression):
    expr1: Expression
    expr2: Expression

# multiplication of two expressions
@dataclass
class MulExpression(Expression):
    expr1: Expression
    expr2: Expression

# division of two expressions
@dataclass
class DivExpression(Expression):
    expr1: Expression
    expr2: Expression

# negation of an expression
@dataclass
class NegatedExpression(Expression):
    expr: Expression

# number node
@dataclass
class Number(Expression):
    value: int

# variable node
@dataclass
class Variable(Expression):
    name: str

# condition built out of expressions
@dataclass
class Condition:
    pass

# condition with > operator
@dataclass
class GreaterThanCondition(Condition):
    expr1: Expression
    expr2: Expression

# condition with < operator
@dataclass
class LessThanCondition(Condition):
    expr1: Expression
    expr2: Expression

# condition with == operator
@dataclass
class EqualsCondition(Condition):
    expr1: Expression
    expr2: Expression

# condition with != operator
@dataclass
class NotEqualsCondition(Condition):
    expr1: Expression
    expr2: Expression

# condition with >= operator
@dataclass
class GreaterThanOrEqualCondition(Condition):
    expr1: Expression
    expr2: Expression

# condition with <= operator
@dataclass
class LessThanOrEqualCondition(Condition):
    expr1: Expression
    expr2: Expression

# statement
@dataclass
class Statement:
    pass

# block of statements
@dataclass
class Block:
    statements: list[Statement]

# data type
class DataType(Enum):
    INT_TYPE = 1
    BOOL_TYPE = 1

# variable declaration
@dataclass
class VarDeclaration(Statement):
    datatype: DataType
    var_name: str
    value: Expression | None

# assignment statement
@dataclass
class Assignment(Statement):
    var_name: str
    value: Expression

# if statement
@dataclass
class IfStatement(Statement):
    condition: Condition 
    true_branch: Block
    false_branch: Block | None

# while loop statement
@dataclass
class WhileStatement(Statement):
    condition: Condition
    loop_body: Block

# for loop statement
@dataclass
class ForStatement(Statement):
    initial: VarDeclaration | Statement
    condition: Condition
    increment: Statement 
    loop_body: Block

# variable registry tuple
@dataclass
class VariableInfo:
    initialised: bool
    datatype: DataType

class CompileError(Exception):
    pass


"""
AST parser class
"""


@v_args(inline=True)
class ASTBuilder(Transformer):
    """
        builds the AST
    """

    def __init__(self):
        self.__var_registry: dict[str, VariableInfo] = {} # initialise variable registry


    def block(self, *statements) -> Block:
        return Block(list(statements))


    def int_type(self) -> DataType:
        return DataType.INT_TYPE


    def bool_type(self) -> DataType:
        return DataType.BOOL_TYPE


    def var_declaration(self, datatype, var_name) -> VarDeclaration:
        if var_name in self.__var_registry:
            raise CompileError(f"Variable `{var_name}` already initialised.")
        self.__var_registry[var_name] = VariableInfo(True, datatype)

        return VarDeclaration(datatype, var_name, None)


    def var_declaration_with_value(self, datatype, var_name, value) -> VarDeclaration:
        if var_name in self.__var_registry:
            raise CompileError(f"Variable `{var_name}` already initialised")
        self.__var_registry[var_name] = VariableInfo(True, datatype)

        return VarDeclaration(datatype, var_name, value)


    def assignment(self, var_name, var_expression) -> Assignment:
        if var_name not in self.__var_registry:
            raise CompileError(f"Variable `{var_name}` missing data type")

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