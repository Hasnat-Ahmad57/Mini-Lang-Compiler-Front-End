# Mini-Lang-Compiler-Front-End
A front-end compiler for MiniLang++, a simplified C-like imperative language. Implements lexical analysis, recursive-descent parsing, semantic analysis with scoped symbol tables, and three-address code (TAC) generation.
✨ Key Features
🔤 Lexical Analysis
Tokenizes MiniLang++ code using regex-based pattern matching, identifying keywords, identifiers, numbers, operators, and delimiters.

🌳 Syntax Analysis (Parsing)
Implements a recursive descent parser (LL(1)) that constructs an Abstract Syntax Tree (AST) from valid source code.

🧠 Semantic Analysis
Builds scoped symbol tables and performs type checking, function verification, and return-type validation.

📦 Intermediate Code Generation
Generates Three-Address Code (TAC) including:

Arithmetic expressions

Variable declarations and assignments

if-else conditions

while loops

Function calls with arguments

🔧 Supported Language Features
✅ int, float, bool types

✅ Variable declarations and assignments

✅ Arithmetic and logical expressions

✅ Control structures: if, else, while

✅ Typed function declarations and returns

✅ Scope-aware symbol resolution

✅ Intermediate TAC output

Example Code (MiniLang++)

int max(int a, int b) {
  if (a > b) {
    return a;
  } else {
    return b;
  }
}

int main() {
  int x = 5;
  int y = 10;
  int z = max(x, y);
  return z;
}

Built With
🐍 Python 3

📐 Regular Expressions for Tokenization

🧩 Recursive Descent Parsing

🗂️ Scoped Symbol Tables

📜 Label-based TAC generation

