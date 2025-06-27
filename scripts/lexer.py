import re

TOKEN_SPEC = [
    ('COMMENT', r'//.*'),  # Comments (ignored)
    ('NUMBER', r'\d+(\.\d*)?'),  # Integer or float
    ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
    ('OP', r'[+\-*/=<>]'),  # Operators
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMI', r';'),
    ('COMMA', r','),
    ('WS', r'\s+'),  # Whitespace (ignored)
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

KEYWORDS = {'int', 'float', 'bool', 'if', 'else', 'while', 'return'}


def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0

    for mo in re.finditer(TOKEN_REGEX, code):
        kind = mo.lastgroup
        value = mo.group()
        start = mo.start()
        end = mo.end()

        # Count line number & column
        line_num += code[line_start:start].count('\n')
        if '\n' in code[line_start:start]:
            line_start = code.rfind('\n', line_start, start) + 1

        column = start - line_start + 1

        if kind in ['WS', 'COMMENT']:
            continue

        if kind == 'ID' and value in KEYWORDS:
            kind = value.upper()

        tokens.append((kind, value))

    # Check for unmatched characters
    combined_pattern = re.compile(TOKEN_REGEX)
    pos = 0
    while pos < len(code):
        match = combined_pattern.match(code, pos)
        if match:
            pos = match.end()
        else:
            # Report invalid character with line/column
            line = code[:pos].count('\n') + 1
            col = pos - code.rfind('\n', 0, pos)
            print(f"❌ Lexical Error: Invalid character '{code[pos]}' at line {line}, column {col}")
            pos += 1  # Skip invalid char and keep scanning

    return tokens
