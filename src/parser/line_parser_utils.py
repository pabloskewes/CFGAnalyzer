def clean_string(string: str) -> str:
    string = string.replace("    ", "\t").replace("’", "'")
    return string


def is_var(var: str) -> bool:
    return var.isalpha() and var.islower() and len(var) == 1


def is_constant(constant: str) -> bool:
    return constant.isnumeric() or constant == "True" or constant == "False"


def is_string(string: str) -> bool:
    double_quote = string.startswith('"') and string.endswith('"')
    single_quote = string.startswith("'") and string.endswith("'")
    return double_quote or single_quote


def is_function_call(call: str) -> bool:
    if "(" not in call or not call.endswith(")"):
        return False
    func_name, args = call.split("(")[0], call.split("(")[1].split(")")[0]
    if not func_name.isalpha():
        return False

    if not args:
        return True

    for arg in args.split(","):
        arg = arg.strip()
        if not is_expression(arg) and not is_string(arg):
            return False

    return True


def is_expression(expr: str) -> bool:
    expr = expr.strip()

    # Check for variables and constants
    if is_var(expr) or is_constant(expr):
        return True

    # Check for function calls
    if "(" in expr and expr.endswith(")"):
        if is_function_call(expr):
            return True

    # Check for binary operations
    for op in ["+", "-", "*", "/", "%", "**"]:
        if op in expr:
            parts = expr.split(op, 1)
            left_expr, right_expr = parts[0].strip(), parts[1].strip()
            if is_expression(left_expr) and is_expression(right_expr):
                return True

    # Check for nested expressions
    if "(" in expr and ")" in expr:
        opening_index = expr.find("(")
        closing_index = expr.rfind(")")
        nested_expr = expr[opening_index + 1 : closing_index].strip()
        return is_expression(nested_expr)

    return False


def is_condition(cond: str) -> bool:
    cond = cond.strip()

    for op in ["==", "!=", "<", ">", "<=", ">="]:
        if op in cond:
            parts = cond.split(op, 1)
            left_expr, right_expr = parts[0].strip(), parts[1].strip()
            if is_expression(left_expr) and is_expression(right_expr):
                return True


def is_assignment(assignment: str) -> bool:
    assignment = assignment.strip()

    if "=" not in assignment:
        return False

    parts = assignment.split("=", 1)
    var, expr = parts[0].strip(), parts[1].strip()

    return is_var(var) and is_expression(expr)
