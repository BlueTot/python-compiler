from lark import Transformer, v_args
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


    def var_declaration(self, datatype, var_name) -> VarDeclaration:
        return VarDeclaration(datatype, var_name, None)


    def var_declaration_with_value(self, datatype, var_name, value) -> VarDeclaration:
        return VarDeclaration(datatype, var_name, value)


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


