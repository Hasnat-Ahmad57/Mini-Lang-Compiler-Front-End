from scripts.ast import *
from scripts.lexer import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ('EOF', '')

    def advance(self):
        if self.position < len(self.tokens):
            self.position += 1

    def match(self, expected_type):
        tok_type, value = self.current()
        if tok_type == expected_type:
            self.advance()
            return value
        else:
            self.errors.append(f"❌ Syntax Error: Expected {expected_type} but got {tok_type} ('{value}')")
            return None

    def parse(self):
        functions = []
        while self.current()[0] != 'EOF':
            try:
                func = self.parse_function()
                if func:
                    functions.append(func)
            except Exception as e:
                self.errors.append(f"❌ Parse Error: {str(e)}")
                self.synchronize()
        return Program(functions=functions)

    def synchronize(self):
        sync_tokens = {'INT', 'FLOAT', 'BOOL', 'ID', 'RETURN', 'IF', 'WHILE', 'RBRACE', 'SEMI'}
        while self.current()[0] not in sync_tokens and self.current()[0] != 'EOF':
            self.advance()

    def parse_function(self):
        tok_type, _ = self.current()
        if tok_type not in ['INT', 'FLOAT', 'BOOL']:
            raise SyntaxError(f"Expected return type (INT/FLOAT/BOOL), got {tok_type}")
        self.match(tok_type)
        return_type = tok_type.lower()

        name = self.match('ID') or "unnamed_func"
        self.match('LPAREN')
        params = self.parse_params()
        self.match('RPAREN')
        self.match('LBRACE')
        body = []
        while self.current()[0] != 'RBRACE' and self.current()[0] != 'EOF':
            try:
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            except Exception as e:
                self.errors.append(f"❌ Statement Error: {str(e)}")
                self.synchronize()
        self.match('RBRACE')
        return Function(return_type, name, params, body)

    def parse_params(self):
        params = []
        if self.current()[0] == 'RPAREN':
            return params
        while True:
            tok_type, _ = self.current()
            if tok_type not in ['INT', 'FLOAT', 'BOOL']:
                break
            self.match(tok_type)
            param_type = tok_type.lower()
            param_name = self.match('ID') or "param"
            params.append(Param(param_type, param_name))
            if self.current()[0] != 'COMMA':
                break
            self.match('COMMA')
        return params

    def parse_statement(self):
        tok_type, _ = self.current()
        if tok_type in ['INT', 'FLOAT', 'BOOL']:
            return self.parse_var_decl()
        elif tok_type == 'RETURN':
            return self.parse_return()
        elif tok_type == 'IF':
            return self.parse_if_statement()
        elif tok_type == 'WHILE':
            return self.parse_while_statement()
        else:
            return self.parse_expression_stmt()

    def parse_var_decl(self):
        tok_type, _ = self.current()
        self.match(tok_type)
        var_type = tok_type.lower()
        name = self.match('ID') or "var"
        self.match('OP')
        expr = self.parse_expression()
        self.match('SEMI')
        return Statement(f"declare {var_type} {name}", expression=expr)

    def parse_return(self):
        self.match('RETURN')
        expr = self.parse_expression()
        self.match('SEMI')
        return Statement("return x", expression=expr)

    def parse_expression_stmt(self):
        left = self.match('ID') or "unknown"
        self.match('OP')
        expr = self.parse_expression()
        self.match('SEMI')
        return Statement(f"expr {left} =", expression=expr)

    def parse_if_statement(self):
        self.match('IF')
        self.match('LPAREN')
        condition = self.parse_expression()
        self.match('RPAREN')
        self.match('LBRACE')
        true_branch = []
        while self.current()[0] != 'RBRACE' and self.current()[0] != 'EOF':
            true_branch.append(self.parse_statement())
        self.match('RBRACE')

        false_branch = None
        if self.current()[0] == 'ELSE':
            self.match('ELSE')
            self.match('LBRACE')
            false_branch = []
            while self.current()[0] != 'RBRACE' and self.current()[0] != 'EOF':
                false_branch.append(self.parse_statement())
            self.match('RBRACE')
        return Statement("if", if_stmt=IfStatement(condition, true_branch, false_branch))

    def parse_while_statement(self):
        self.match('WHILE')
        self.match('LPAREN')
        condition = self.parse_expression()
        self.match('RPAREN')
        self.match('LBRACE')
        body = []
        while self.current()[0] != 'RBRACE' and self.current()[0] != 'EOF':
            body.append(self.parse_statement())
        self.match('RBRACE')
        return Statement("while", while_stmt=WhileStatement(condition, body))

    def parse_args(self):
        args = []
        if self.current()[0] == 'RPAREN':
            return args
        args.append(self.match('ID'))
        while self.current()[0] == 'COMMA':
            self.match('COMMA')
            args.append(self.match('ID'))
        return args

    def parse_expression(self):
        return self.parse_term()

    def parse_term(self):
        expr = self.parse_factor()
        while self.current()[0] == 'OP' and self.current()[1] in ['+', '-']:
            op = self.match('OP')
            right = self.parse_factor()
            expr = Expression(expr, op, right)
        return expr

    def parse_factor(self):
        expr = self.parse_primary()
        while self.current()[0] == 'OP' and self.current()[1] in ['*', '/']:
            op = self.match('OP')
            right = self.parse_primary()
            expr = Expression(expr, op, right)
        return expr

    def parse_primary(self):
        tok_type, value = self.current()
        if tok_type == 'ID':
            return self.match('ID')
        elif tok_type == 'NUMBER':
            return self.match('NUMBER')
        elif tok_type == 'LPAREN':
            self.match('LPAREN')
            expr = self.parse_expression()
            self.match('RPAREN')
            return expr
        else:
            self.errors.append(f"❌ Unexpected token: {tok_type} ('{value}')")
            self.advance()
            return "0"  # Fallback for parsing to continue

# External use
def parse(tokens):
    parser = Parser(tokens)
    ast = parser.parse()
    if parser.errors:
        print("\n🛑 Parser Errors:")
        for err in parser.errors:
            print(err)
    return ast
