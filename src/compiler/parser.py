from lark import Transformer, v_args, Token
from dataclasses import dataclass
from .ast_nodes import *


# variable registry tuple
@dataclass
class VariableInfo:
    initialised: bool
    datatype: DataType

class CompileError(Exception):
    pass



@v_args(inline=True)
class ASTBuilder(Transformer):
    """
        class that parses the grammar into an AST
        performs no semantic analysis at all
    """

    def program(self, block) -> Program:
        return Program(block)


    def block(self, *statements) -> Block:
        return Block(list(statements))


    def int_type(self) -> DataType:
        return DataType.INT_TYPE


    def bool_type(self) -> DataType:
        return DataType.BOOL_TYPE


    def var_declaration(self, datatype, var_name_token: Token) -> VarDeclaration:
        return VarDeclaration(datatype, var_name_token.value, None)


    def var_declaration_with_value(self, datatype, var_name_token: Token, value) -> VarDeclaration:
        return VarDeclaration(datatype, var_name_token.value, value)


    def assignment(self, var_name_token: Token, var_expression) -> Assignment:
        return Assignment(var_name_token.value, var_expression)


    def if_only_statement(self, condition, if_block) -> IfStatement:
        return IfStatement(condition, if_block, None)


    def if_and_else_statement(self, condition, if_block, else_block) -> IfStatement:
        return IfStatement(condition, if_block, else_block)


    def while_statement(self, condition, loop_block) -> WhileStatement:
        return WhileStatement(condition, loop_block)


    def for_statement(self, initial, condition, increment, loop_block) -> ForStatement:
        return ForStatement(initial, condition, increment, loop_block)


    # logical or - precdence level 1
    def logical_or(self, expr1, expr2) -> Expression:
        return LogicalOrExpression(expr1, expr2)


    # logical and - precedence level 2
    def logical_and(self, expr1, expr2) -> Expression:
        return LogicalAndExpression(expr1, expr2)


    # bitwise or - precedence level 3
    def bitwise_or(self, expr1, expr2) -> Expression:
        return BitwiseOrExpression(expr1, expr2)


    # bitwise xor - precedence level 4
    def bitwise_xor(self, expr1, expr2) -> Expression:
        return BitwiseXorExpression(expr1, expr2)


    # bitwise and - precedence level 5
    def bitwise_and(self, expr1, expr2) -> Expression:
        return BitwiseAndExpression(expr1, expr2)


    # eqaulity operator - precedence level 6
    def equal_to(self, expr1, expr2) -> Expression:
        return EqualsExpression(expr1, expr2)


    # not equal operator - precedence level 6
    def not_equal_to(self, expr1, expr2) -> Expression:
        return NotEqualsExpression(expr1, expr2)


    # greater than operator - precedence level 7
    def greater_than(self, expr1, expr2) -> Expression:
        return GreaterThanExpression(expr1, expr2)


    # less than operator - precedence level 7
    def less_than(self, expr1, expr2) -> Expression:
        return LessThanExpression(expr1, expr2)


    # greater than or equal operator - precedence level 7
    def greater_than_equal(self, expr1, expr2) -> Expression:
        return GreaterThanOrEqualExpression(expr1, expr2)


    # less than or equal operator - precedence level 7
    def less_than_equal(self, expr1, expr2) -> Expression:
        return LessThanOrEqualExpression(expr1, expr2)

    # bitwise left shift operator - precedence level 8
    def bitwise_left_shift(self, expr1, expr2) -> Expression:
        return BitwiseLeftShift(expr1, expr2)


    # bitwise right shift operator - precedence level 8
    def bitwise_right_shift(self, expr1, expr2) -> Expression:
        return BitwiseRightShift(expr1, expr2)


    # addition operator - precedence level 9
    def add(self, expr1, expr2) -> Expression:
        return AddExpression(expr1, expr2)


    # subtraction operator - precedence level 9
    def sub(self, expr1, expr2) -> Expression:
        return SubExpression(expr1, expr2)


    # multiplication operator - precedence level 10
    def mul(self, expr1, expr2) -> Expression:
        return MulExpression(expr1, expr2)


    # multiplication operator - precedence level 10
    def div(self, expr1, expr2) -> Expression:
        return DivExpression(expr1, expr2)

    
    # logical not operator - precedence level 11
    def logical_not(self, expr) -> Expression:
        return LogicalNotExpression(expr)


    # bitwise not operator - precedence level 11
    def bitwise_not(self, expr) -> Expression:
        return BitwiseNotExpression(expr)


    # unary negation operator - precedence level 11
    def neg(self, expr) -> Expression:
        return NegatedExpression(expr)


    # number token
    def number(self, token: Token) -> Expression:
        return Number(token.value)


    # true literal
    def true(self) -> Expression:
        return BooleanConstant(True)

    
    # false literal
    def false(self) -> Expression:
        return BooleanConstant(False)


    # variable token
    def var(self, token: Token) -> Expression:
        return Variable(token.value)


