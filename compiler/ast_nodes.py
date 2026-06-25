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

# program
@dataclass
class Program:
    block: Block

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
