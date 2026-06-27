from dataclasses import dataclass
from .ast_nodes import *


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
        print(ast)
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

            else:
                raise Exception("Something went wrong")

        return initialised


    def __lookup_variable(self, var_name: str, scopes: list[dict[str, SymbolData]]) -> SymbolData:
        """
            Looks up a variable name in the stack of scopes (newest at top),
            raising an error if the variable does not exist
        """

        for scope in reversed(scopes):
            if var_name in scope:
                return scope[var_name]

        raise SemanticError(f"Variable '{var_name}' is not declared")


    def __check_expression(self, expr: Expression, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> DataType:
        """
            Checks if an expression is valid, requiring:
            1. variables used must exist and be initialised
            2. types must match

            Returns the data type of the expression if valid
            Raises a SemanticError if not valid
        """ 

        # logical or expression (bool || bool -> bool), level 1
        if isinstance(expr, LogicalOrExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, BoolType) and isinstance(type2, BoolType):
                return BoolType()
            raise SemanticError("Operator '||' requires bool operands")
        
        # logical and expression (bool && bool -> bool), level 2
        elif isinstance(expr, LogicalAndExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)
            print(expr.expr1, expr.expr2, type1, type2)

            if isinstance(type1, BoolType) and isinstance(type2, BoolType):
                return BoolType()
            print("HEYY")
            raise SemanticError("Operator '&&' requires bool operands")

        # bitwise or expression (int | int -> int), level 3
        elif isinstance(expr, BitwiseOrExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '|' requires int operands")

        # bitwise xor expression (int ^ int -> int), level 4
        elif isinstance(expr, BitwiseXorExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '^' requires int operands")
            
        # bitwise and expression (int & int -> int), level 5
        elif isinstance(expr, BitwiseAndExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '&' requires int operands")

        # equals expression (any == any -> bool), level 6
        elif isinstance(expr, EqualsExpression):
            _ = self.__check_expression(expr.expr1, scopes, initialised)
            _ = self.__check_expression(expr.expr2, scopes, initialised)
            return BoolType()

        # equals expression (any != any -> bool), level 6
        elif isinstance(expr, NotEqualsExpression):
            _ = self.__check_expression(expr.expr1, scopes, initialised)
            _ = self.__check_expression(expr.expr2, scopes, initialised)
            return BoolType()

        # greater than expression (int > int -> bool), level 7
        elif isinstance(expr, GreaterThanExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return BoolType()
            raise SemanticError("Operator '>' requires int operands")

        # less than expression (int < int -> int), level 7
        elif isinstance(expr, LessThanExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return BoolType()
            raise SemanticError("Operator '<' requires int operands")

        # greater than or equal expression (int >= int -> int), level 7
        elif isinstance(expr, GreaterThanOrEqualExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return BoolType()
            raise SemanticError("Operator '>=' requires int operands")

        # less than or equal expression (int <= int -> int), level 7
        elif isinstance(expr, LessThanOrEqualExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return BoolType()
            raise SemanticError("Operator '<=' requires int operands")

        # bitwise left shift expression (int << int -> int), level 8
        elif isinstance(expr, BitwiseLeftShift):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '<<' requires int operands")

        # bitwise right shift expression (int >> int -> int), level 8
        elif isinstance(expr, BitwiseRightShift):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '>>' requires int operands")

        # add expression (int + int -> int), level 9
        elif isinstance(expr, AddExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '+' requires int operands")

        # subtraction expression (int - int -> int), level 9
        elif isinstance(expr, SubExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '-' requires int operands")

        # multiplication expression (int * int -> int), level 10
        elif isinstance(expr, MulExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '*' requires int operands")

        # division expression (int / int -> int), level 10
        elif isinstance(expr, DivExpression):
            type1 = self.__check_expression(expr.expr1, scopes, initialised)
            type2 = self.__check_expression(expr.expr2, scopes, initialised)

            if isinstance(type1, IntType) and isinstance(type2, IntType):
                return IntType()
            raise SemanticError("Operator '/' requires int operands")

        # logical not expression (!bool -> bool), level 11
        elif isinstance(expr, LogicalNotExpression): 
            type1 = self.__check_expression(expr.expr, scopes, initialised)

            if isinstance(type1, BoolType):
                return BoolType()
            raise SemanticError("Operator '!' requires bool operand")

        # bitwise not expression (~int -> int), level 11
        elif isinstance(expr, BitwiseNotExpression):
            type1 = self.__check_expression(expr.expr, scopes, initialised)

            if isinstance(type1, IntType):
                return IntType()
            raise SemanticError("Operator '~' requires int operand")

        # negation expression (-int -> int), level 11
        elif isinstance(expr, NegatedExpression):
            type1 = self.__check_expression(expr.expr, scopes, initialised)

            if isinstance(type1, IntType):
                return IntType()
            raise SemanticError("Operator '-' requires int operand")

        elif isinstance(expr, Number):
            print(1)
            return IntType() # number is int type

        elif isinstance(expr, BooleanConstant):
            print(2)
            return BoolType() # true/false is boolean type
            
        elif isinstance(expr, Variable):
            var_name = expr.name
            var_data = self.__lookup_variable(var_name, scopes) # check if variable exists
            if var_name not in initialised: # check if variable is initialised
                raise SemanticError(f"Variable '{var_name}' might be uninitialised")
            return var_data.datatype # return the variable's data type
            
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

        # check if variable exists already
        var_exists: bool = False
        try:
            self.__lookup_variable(declaration.var_name, scopes) 
            var_exists = True
        except SemanticError:
            pass
        if var_exists:
            raise SemanticError(f"Variable '{declaration.var_name}' is already declared")

        if declaration.value is None: # declaration only
            scopes[-1][declaration.var_name] = SymbolData(datatype = declaration.datatype, initialised=False)
        
        else: # declaration + initial assignment
            scopes[-1][declaration.var_name] = SymbolData(datatype = declaration.datatype, initialised=True)
            self.__check_expression(declaration.value, scopes, initialised) # check initial expression
            initialised.add(declaration.var_name)

        return initialised



    def __check_if_statement(self, statement: IfStatement, scopes: list[dict[str, SymbolData]], initialised: set[str]) -> set[str]:
        """
            Checks if an if statement is valid, raises a SemanticError if not. Requires:
            1. condition is valid
            2. true branch is valid
            3. false branch is valid (if it exists)

            Returns modified set of initialised values
        """


        self.__check_expression(statement.condition, scopes, initialised) # check condition is valid

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

        self.__check_expression(loop.condition, scopes, initialised) # check the condition is valid

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
        self.__check_expression(loop.condition, scopes, initialised) # check loop condition is valid
        self.__check_assignment(loop.increment, scopes, initialised) # check loop increment is valid

        self.__check_block(loop.loop_body, scopes + [{}], initialised.copy()) # check loop body is valid

        return initialised

