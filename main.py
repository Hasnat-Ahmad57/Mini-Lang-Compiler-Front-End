import sys
from scripts import lexer, parser, semantic_analyzer
from scripts.parser import Parser
from scripts import intermediate_code
def main():
    with open("test/sample1", "r", encoding="utf-8") as file:

        code = file.read()

    print("📥 Lexing...")
    tokens = lexer.tokenize(code)
    print("📤 Tokens:")
    for tok in tokens:
        print(f"  {tok}")

    print("\n🧱 Parsing...")
    ast = Parser(tokens).parse()

    print("\n🌳 AST Structure:")
    for func in ast.functions:
        print(f"Function: {func.name} -> {func.return_type}")
        if func.params:
            print("  Params:")
            for param in func.params:
                print(f"    {param.param_type} {param.name}")
        print("  Body:")
        for stmt in func.body:
            print(f"    {stmt.value}")

    print("\n🧠 Semantic Analysis:")
    semantic_analyzer.analyze(ast)

    intermediate_code.generate_intermediate_code(ast)


if __name__ == "__main__":
    main()
