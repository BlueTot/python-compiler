from lark import Lark, Transformer, v_args

@v_args(inline=True)
class ASTBuilder(Transformer):
    """
        builds the AST
    """
    pass



parser = Lark.open("./grammar.lark", parser="lalr", transformer=ASTBuilder())


def main() -> None:
    with open("./code.txt") as f:
        program = f.read()
    print(parser.parse(program))

if __name__ == "__main__":
    main()