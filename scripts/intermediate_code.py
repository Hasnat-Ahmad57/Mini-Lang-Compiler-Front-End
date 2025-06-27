from scripts.ast import *

temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def generate_intermediate_code(ast: Program):
    print("\n🧾 Intermediate Code (TAC):")
    for func in ast.functions:
        print(f"# Function: {func.name}")
        for stmt in func.body:
            gen_stmt(stmt)

def gen_stmt(stmt: Statement):
    if stmt.value.startswith("declare"):
        parts = stmt.value.split()
        if len(parts) < 3:
            print(f"❌ Invalid declaration statement: {stmt.value}")
            return
        _, var_type, var_name = parts

        if stmt.expression:
            code, temp = gen_expression(stmt.expression)
            for line in code:
                print(line)
            print(f"{var_name} = {temp}")
        else:
            print(f"❌ Declaration missing expression: {stmt.value}")

    elif stmt.value.startswith("expr"):
        parts = stmt.value.split()
        if len(parts) < 3:
            print(f"❌ Invalid assignment statement: {stmt.value}")
            return
        _, left, _ = parts
        if stmt.expression:
            code, temp = gen_expression(stmt.expression)
            for line in code:
                print(line)
            print(f"{left} = {temp}")
        else:
            print(f"❌ Assignment missing expression: {stmt.value}")

    elif stmt.value.startswith("return"):
        if stmt.expression:
            code, temp = gen_expression(stmt.expression)
            for line in code:
                print(line)
            print(f"return {temp}")
        else:
            parts = stmt.value.split()
            if len(parts) >= 2:
                _, ret_var = parts
                print(f"return {ret_var}")
            else:
                print(f"❌ Invalid return statement: {stmt.value}")

    elif stmt.func_call:
        tmp = new_temp()
        arg_list = ", ".join(stmt.func_call.args)
        print(f"{tmp} = call {stmt.func_call.name}, {arg_list}")
        left = stmt.value.split()[1]  # call z = func()
        print(f"{left} = {tmp}")

    elif stmt.if_stmt:
        label_else = f"L{new_temp()}"
        label_end = f"L{new_temp()}"
        cond_code, cond_temp = gen_expression(stmt.if_stmt.condition)
        for line in cond_code:
            print(line)
        print(f"if_false {cond_temp} goto {label_else}")
        for s in stmt.if_stmt.true_branch:
            gen_stmt(s)
        print(f"goto {label_end}")
        print(f"{label_else}:")
        if stmt.if_stmt.false_branch:
            for s in stmt.if_stmt.false_branch:
                gen_stmt(s)
        print(f"{label_end}:")

    elif stmt.while_stmt:
        label_start = f"L{new_temp()}"
        label_end = f"L{new_temp()}"
        print(f"{label_start}:")
        cond_code, cond_temp = gen_expression(stmt.while_stmt.condition)
        for line in cond_code:
            print(line)
        print(f"if_false {cond_temp} goto {label_end}")
        for s in stmt.while_stmt.body:
            gen_stmt(s)
        print(f"goto {label_start}")
        print(f"{label_end}:")

def gen_expression(expr):
    if isinstance(expr, str):
        return [], expr
    elif isinstance(expr, Expression):
        left_code, left_temp = gen_expression(expr.left)
        right_code, right_temp = gen_expression(expr.right)
        result = new_temp()
        code = left_code + right_code + [f"{result} = {left_temp} {expr.operator} {right_temp}"]
        return code, result
    else:
        return [], str(expr)
