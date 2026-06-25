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

    def check(self, ast: Block) -> None:
        pass

    
    def __check_block(self, block: Block) -> None:
        pass


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
            self.__check_expression(expr.expr1)
            self.__check_expression(expr.expr2)

        elif isinstance(expr, SubExpression):
            self.__check_expression(expr.expr1)
            self.__check_expression(expr.expr2)

        elif isinstance(expr, MulExpression):
            self.__check_expression(expr.expr1)
            self.__check_expression(expr.expr2)

        elif isinstance(expr, DivExpression):
            self.__check_expression(expr.expr1)
            self.__check_expression(expr.expr2)

        elif isinstance(expr, NegatedExpression):
            self.__check_expression(expr)

        elif isinstance(expr, Number):
            pass
            
        elif isinstance(expr, Variable):
            var_name = expr.name
            self.__lookup_variable(var_name, scopes) # check if variable exists
            if var_name not in initialised: # check if variable is initialised
                raise SemanticError(f"Variable `{var_name}` is not initialised")
            
        else:
            raise Exception("something went wrong")


    def __check_assignment(self, assignment: Assignment, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> None:
        """
            Check if a variable assignment statement is valid given the current stack of variable scopes,
            and set of initialised variables. This requires:

            1. variable to exist
            2. expression to be valid
            3. data types to match (TODO)

            Raises a SemanticError if not valid
        """

        self.__lookup_variable(assignment.var_name, scopes)
        self.__check_expression(assignment.value, scopes, initialised)
        


    def __check_declaration(self, declaration: VarDeclaration, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> None:
        """
            Check if a variable declaration statement is valid
            given the current stack of variable scopes,
            and set of initialised variables 

            Raises a SemanticError if not valid
        """

        if declaration.var_name in scopes[-1]: # variable exists already
            raise SemanticError(f"Variable with name `{declaration.var_name} already declared")

        if declaration.value is None: # declaration only
            scopes[declaration.var_name] = SymbolData(datatype = declaration.datatype, initialised=False)
        
        else:
            scopes[declaration.var_name] = SymbolData(datatype = declaration.datatype, initialised=True)

