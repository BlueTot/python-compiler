from dataclasses import dataclass
from ast_nodes import *


class SemanticError(Exception):
    pass


@dataclass
class SymbolData:
    datatype: DataType
    initialised: bool


class SemanticChecker:
    """
        Class that performs semantic analysis of the program, including
        name checking, initialisation checking, and type checking

        VARIABLE SHADOWING IS DISABLED
    """

    def __init__(self):
        pass


    def check(self, ast: Program) -> None:
        """
            Entry point to the semantic checker
            Checks if an AST for a program is valid, raising a SemanticError if not
        """
        self.__check_block(ast.block, [{}], set())

    
    def __check_block(self, block: Block, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Checks if a block of code is valid, raising a SemanticError if not
            Returns set of initialised variables
        """

        for statement in block.statements: # iterate through all statements in the block

            if isinstance(statement, VarDeclaration):
                initialised = self.__check_declaration(statement, scopes, initialised)

            elif isinstance(statement, Assignment):
                initialised = self.__check_assignment(statement, scopes, initialised)

            elif isinstance(statement, IfStatement):
                initialised = self.__check_if_statement(statement, scopes, initialised)

            elif isinstance(statement, WhileStatement):
                initialised = self.__check_while_loop(statement, scopes, initialised)

            elif isinstance(statement, ForStatement):
                initialised = self.__check_for_loop(statement, scopes, initialised)

        return initialised


    def __lookup_variable(self, var_name: str, scopes: list[dict[str, SymbolData]]) -> SymbolData:
        """
            Looks up a variable name in the stack of scopes (newest at top),
            raising an error if the variable does not exist
        """

        for scope in reversed(scopes):
            if var_name in scope:
                return scope[var_name]

        raise SemanticError(f"Variable `{var_name}` does not exist")


    def __check_expression(self, expr: Expression, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> None:
        """
            Checks if an expression is valid, requiring:
            1. variables used must exist and be initialised
            2. types must match (TODO)

            Raises a SemanticError if not valid
        """ 

        if isinstance(expr, AddExpression):
            self.__check_expression(expr.expr1, scopes, initialised)
            self.__check_expression(expr.expr2, scopes, initialised)

        elif isinstance(expr, SubExpression):
            self.__check_expression(expr.expr1, scopes, initialised)
            self.__check_expression(expr.expr2, scopes, initialised)

        elif isinstance(expr, MulExpression):
            self.__check_expression(expr.expr1, scopes, initialised)
            self.__check_expression(expr.expr2, scopes, initialised)

        elif isinstance(expr, DivExpression):
            self.__check_expression(expr.expr1, scopes, initialised)
            self.__check_expression(expr.expr2, scopes, initialised)

        elif isinstance(expr, NegatedExpression):
            self.__check_expression(expr.expr, scopes, initialised)

        elif isinstance(expr, Number):
            pass
            
        elif isinstance(expr, Variable):
            var_name = expr.name
            self.__lookup_variable(var_name, scopes) # check if variable exists
            if var_name not in initialised: # check if variable is initialised
                raise SemanticError(f"Variable `{var_name}` is not initialised")
            
        else:
            raise Exception("something went wrong")



    def __check_assignment(self, assignment: Assignment, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Check if a variable assignment statement is valid given the current stack of variable scopes,
            and set of initialised variables. This requires:

            1. variable to exist
            2. expression to be valid
            3. data types to match (TODO)

            Raises a SemanticError if not valid
            Returns the modified set of initialised values
        """
        
        self.__lookup_variable(assignment.var_name, scopes)
        self.__check_expression(assignment.value, scopes, initialised)
        initialised.add(assignment.var_name) # add to set of initialised values

        return initialised
        


    def __check_declaration(self, declaration: VarDeclaration, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Check if a variable declaration statement is valid
            given the current stack of variable scopes,
            and set of initialised variables 

            Raises a SemanticError if not valid
            Returns the modified set of initialised values
        """

        if declaration.var_name in scopes[-1]: # variable exists already
            raise SemanticError(f"Variable with name `{declaration.var_name} already declared")

        if declaration.value is None: # declaration only
            scopes[-1][declaration.var_name] = SymbolData(datatype = declaration.datatype, initialised=False)
        
        else:
            scopes[-1][declaration.var_name] = SymbolData(datatype = declaration.datatype, initialised=True)
            initialised.add(declaration.var_name)

        return initialised


    def __check_condition(self, condition: Condition, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> None:
        """
            Check if a condition is valid, raises a SemanticError if not valid. Requires:
            1. two sides of comparator are valid expressions
            2. boolean operation can be applied (TODO)
        """

        if isinstance(condition, GreaterThanCondition):
            self.__check_expression(condition.expr1, scopes, initialised)
            self.__check_expression(condition.expr2, scopes, initialised)
            
        elif isinstance(condition, LessThanCondition):
            self.__check_expression(condition.expr1, scopes, initialised)
            self.__check_expression(condition.expr2, scopes, initialised)

        elif isinstance(condition, GreaterThanOrEqualCondition):
            self.__check_expression(condition.expr1, scopes, initialised)
            self.__check_expression(condition.expr2, scopes, initialised)

        elif isinstance(condition, LessThanOrEqualCondition):
            self.__check_expression(condition.expr1, scopes, initialised)
            self.__check_expression(condition.expr2, scopes, initialised)

        elif isinstance(condition, EqualsCondition):
            self.__check_expression(condition.expr1, scopes, initialised)
            self.__check_expression(condition.expr2, scopes, initialised)

        elif isinstance(condition, NotEqualsCondition):
            self.__check_expression(condition.expr1, scopes, initialised)
            self.__check_expression(condition.expr2, scopes, initialised)

        else:
            raise Exception("Unexpected error")


    def __check_if_statement(self, statement: IfStatement, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Checks if an if statement is valid, raises a SemanticError if not. Requires:
            1. condition is valid
            2. true branch is valid
            3. false branch is valid (if it exists)

            Returns modified set of initialised values
        """


        self.__check_condition(statement.condition, scopes, initialised) # check condition is valid

        true_initialised = self.__check_block(statement.true_branch, scopes + [{}], initialised.copy()) # add new scope!!

        if statement.false_branch is not None: # check false branch if it exists
            false_initialised = self.__check_block(statement.false_branch, scopes + [{}], initialised.copy()) # add new scope!!
        else:
            false_initialised = initialised # if the branch doesn't exist

        return true_initialised & false_initialised # variable initialised only if initialised in both


    def __check_while_loop(self, loop: WhileStatement, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Checks if a while loop is valid, raises a SemanticError if not. Requires:
            1. condition is valid
            2. loop body is valid

            Returns modified set of initialised values
        """

        self.__check_condition(loop.condition, scopes, initialised) # check the condition is valid

        self.__check_block(loop.loop_body, scopes + [{}], initialised.copy()) # check the loop body

        return initialised


    def __check_for_loop(self, loop: ForStatement, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Checks if a for loop is valid, raises a SemanticError if not. Requires:    
            1. three for loop statements are valid
            2. loop body is valid

            Returns set of initialised values
        """

        self.__check_assignment(loop.initial, scopes, initialised) # check initial statement is valid
        self.__check_condition(loop.condition, scopes, initialised) # check loop condition is valid
        self.__check_assignment(loop.increment, scopes, initialised) # check loop increment is valid

        self.__check_block(loop.loop_body, scopes + [{}], initialised.copy()) # check loop body is valid

        return initialised

