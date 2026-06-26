from dataclasses import dataclass
from enum import Enum

"""
Dataclasses for AST nodes
"""

# arithemtic expression
@dataclass
class Expression:
    pass

# logical OR of two expressions (level 1)
@dataclass
class LogicalOrExpression(Expression):
    expr1: Expression
    expr2: Expression

# logical AND of two expressions (level 2)
@dataclass
class LogicalAndExpression(Expression):
    expr1: Expression
    expr2: Expression

# bitwise OR of two expressions (level 3)
@dataclass
class BitwiseOrExpression(Expression):
    expr1: Expression
    expr2: Expression

# bitwise XOR of two expressions (level 4)
@dataclass
class BitwiseXorExpression(Expression):
    expr1: Expression
    expr2: Expression

# bitwise AND of two expressions (level 5)
class BitwiseAndExpression(Expression):
    expr1: Expression
    expr2: Expression

# expression with == operator (level 6)
@dataclass
class EqualsExpression(Expression):
    expr1: Expression
    expr2: Expression

# expression with != operator (level 6)
@dataclass
class NotEqualsExpression(Expression):
    expr1: Expression
    expr2: Expression


# expression with > operator (level 7)
@dataclass
class GreaterThanExpression(Expression):
    expr1: Expression
    expr2: Expression

# expression with < operator (level 7)
@dataclass
class LessThanExpression(Expression):
    expr1: Expression
    expr2: Expression

# expression with >= operator (level 7)
@dataclass
class GreaterThanOrEqualExpression(Expression):
    expr1: Expression
    expr2: Expression

# expression with <= operator (level 7)
@dataclass
class LessThanOrEqualExpression(Expression):
    expr1: Expression
    expr2: Expression

# addition of two expressions (level 8)
@dataclass
class AddExpression(Expression):
    expr1: Expression
    expr2: Expression

# subtraction of two expressions (level 8)
@dataclass
class SubExpression(Expression):
    expr1: Expression
    expr2: Expression

# multiplication of two expressions (level 9)
@dataclass
class MulExpression(Expression):
    expr1: Expression
    expr2: Expression

# division of two expressions (level 9)
@dataclass
class DivExpression(Expression):
    expr1: Expression
    expr2: Expression

# logical NOT of an expression (level 10)
@dataclass
class LogicalNotExpression(Expression):
    expr: Expression

# bitwise NOT of an expression (level 10)
@dataclass
class BitwiseNotExpression(Expression):
    expr: Expression

# negation of an expression (level 10)
@dataclass
class NegatedExpression(Expression):
    expr: Expression

# number expression
@dataclass
class Number(Expression):
    value: int

# variable expression
@dataclass
class Variable(Expression):
    name: str

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
    condition: Expression 
    true_branch: Block
    false_branch: Block | None

# while loop statement
@dataclass
class WhileStatement(Statement):
    condition: Expression 
    loop_body: Block

# for loop statement
@dataclass
class ForStatement(Statement):
    initial: Assignment
    condition: Expression 
    increment: Assignment 
    loop_body: Block
