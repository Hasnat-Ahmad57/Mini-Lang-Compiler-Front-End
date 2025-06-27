from scripts.symbol_table import SymbolTable
from scripts.ast import *

def analyze(ast: Program):
    print("Semantic analysis in progress...")
    symtab = SymbolTable()
    function_signatures = {}
    had_error = False

    for func in ast.functions:
        try:
            symtab.declare(func.name, func.return_type)
            param_types = [p.param_type for p in func.params]
            function_signatures[func.name] = (param_types, func.return_type)
        except Exception as e:
            print(e)
            had_error = True

    for func in ast.functions:
        symtab.enter_scope()
        for param in func.params:
            try:
                symtab.declare(param.name, param.param_type)
            except Exception as e:
                print(e)
                had_error = True
        for stmt in func.body:
            if analyze_statement(stmt, symtab, func.return_type, function_signatures):
                had_error = True
        symtab.exit_scope()

    if not had_error:
        print("✅ Semantic analysis completed successfully.")
    else:
        print("❌ Semantic analysis completed with errors.")

def analyze_statement(stmt: Statement, symtab: SymbolTable, expected_return_type=None, function_signatures=None):
    error = False

    if stmt.value.startswith("declare"):
        parts = stmt.value.split()
        if len(parts) < 3:
            print(f"❌ Invalid declaration statement: {stmt.value}")
            return True
        _, var_type, name = parts
        try:
            symtab.declare(name, var_type)
        except Exception as e:
            print(e)
            error = True

        if stmt.expression:
            if isinstance(stmt.expression, str):
                if var_type == "int" and "." in stmt.expression:
                    print(f"❌ Type mismatch: assigning float to int variable '{name}'.")
                    error = True

    elif stmt.value.startswith("expr"):
        parts = stmt.value.split()
        if len(parts) < 3:
            print(f"❌ Invalid assignment statement: {stmt.value}")
            return True
        _, left, _ = parts

        if stmt.expression:
            try:
                _ = symtab.lookup(left)
            except Exception as e:
                print(e)
                error = True

    elif stmt.value.startswith("return"):
        if stmt.expression:
            ret_type = None
            if isinstance(stmt.expression, str):
                if stmt.expression.replace(".", "", 1).isdigit():
                    ret_type = "float" if "." in stmt.expression else "int"
                else:
                    try:
                        ret_type = symtab.lookup(stmt.expression)
                    except Exception as e:
                        print(e)
                        return True
            else:
                ret_type = expected_return_type

            if expected_return_type and ret_type != expected_return_type:
                print(f"❌ Return type mismatch: function expects {expected_return_type}, but returning {ret_type}")
                error = True

    elif stmt.func_call:
        func = stmt.func_call
        if func.name not in function_signatures:
            print(f"❌ Function '{func.name}' is not declared.")
            return True

        expected_params, return_type = function_signatures[func.name]
        left_var = stmt.value.split()[1]

        if not symtab.exists(left_var):
            try:
                symtab.declare(left_var, return_type)
            except Exception as e:
                print(e)
                error = True

        if len(func.args) != len(expected_params):
            print(f"❌ Argument count mismatch in call to '{func.name}': expected {len(expected_params)}, got {len(func.args)}")
            return True

        for i, arg in enumerate(func.args):
            try:
                arg_type = symtab.lookup(arg)
                if arg_type != expected_params[i]:
                    print(f"❌ Argument type mismatch in call to '{func.name}': expected {expected_params[i]}, got {arg_type}")
                    error = True
            except Exception as e:
                print(f"❌ Argument '{arg}' in call to '{func.name}' is not declared.")
                error = True

    elif stmt.if_stmt:
        cond = stmt.if_stmt.condition
        try:
            cond_type = symtab.lookup(cond) if isinstance(cond, str) else 'int'
            if cond_type not in ['int', 'bool']:
                print(f"❌ Condition must be int or bool, got {cond_type}")
                error = True
        except Exception:
            print(f"❌ Condition variable in if-statement is not declared.")
            error = True

        symtab.enter_scope()
        for s in stmt.if_stmt.true_branch:
            if analyze_statement(s, symtab, expected_return_type, function_signatures):
                error = True
        symtab.exit_scope()

        if stmt.if_stmt.false_branch:
            symtab.enter_scope()
            for s in stmt.if_stmt.false_branch:
                if analyze_statement(s, symtab, expected_return_type, function_signatures):
                    error = True
            symtab.exit_scope()

    elif stmt.while_stmt:
        cond = stmt.while_stmt.condition
        try:
            cond_type = symtab.lookup(cond) if isinstance(cond, str) else 'int'
            if cond_type not in ['int', 'bool']:
                print(f"❌ Condition must be int or bool, got {cond_type}")
                error = True
        except Exception:
            print(f"❌ Condition variable in while-loop is not declared.")
            error = True

        symtab.enter_scope()
        for s in stmt.while_stmt.body:
            if analyze_statement(s, symtab, expected_return_type, function_signatures):
                error = True
        symtab.exit_scope()

    return error
