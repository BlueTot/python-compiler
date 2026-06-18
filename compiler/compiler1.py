from lark import Lark, Transformer, v_args

@v_args(inline=True)
class ASTBuilder(Transformer):
    """
        builds the AST
    """
    pass



parser = Lark.open("./grammar.lark", parser="lalr", transformer=ASTBuilder())


def main() -> None:
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(parser.parse(s))

if __name__ == "__main__":
    main()