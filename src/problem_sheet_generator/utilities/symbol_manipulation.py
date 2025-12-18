from sympy import Symbol, Expr, Pow, Mul, Number, Add, S, expand, factor_terms, factor
from sympy.vector import CoordSys3D, BaseScalar

# TODO: Write docstrings
# TODO: Combine logic of scalar-from-expr and expr-from-scalar

def _scalar_from_symbol(sym: Symbol, C: CoordSys3D) -> BaseScalar:
    for scalar in C.base_scalars():
            if str(sym) == str(scalar)[-1]:
                return scalar

def _scalar_expr_from_mul(expr: Expr, C: CoordSys3D) -> Expr:
    args = expr.args
    if isinstance(expr, Pow):
        return _scalar_from_symbol(args[0], C)**args[1]

    expr_has_coeff = isinstance(args[0], (Number, int))
    variables = args[1:] if expr_has_coeff else args
    new_expr = args[0] if expr_has_coeff else S.One

    for var in variables:
        if isinstance(var, Pow):
            new_expr *= _scalar_from_symbol(var.args[0], C)**var.args[1]

        else:
            new_expr *= _scalar_from_symbol(var, C)

    return new_expr

def scalar_expr_from_expr(expr: Expr, C: CoordSys3D) -> Expr:
    if (not hasattr(expr, "free_symbols") or
        not expr.free_symbols or
        hasattr(next(iter(expr.free_symbols)), "system")):
        return expr

    expr = expand(expr)
    if isinstance(expr, Symbol):
        return _scalar_from_symbol(expr, C)

    elif isinstance(expr, (Mul, Pow)):
        return _scalar_expr_from_mul(expr, C)

    elif isinstance(expr, Add):
        new_expr = S.Zero
        for arg in expr.args:
            if isinstance(arg, Symbol):
                new_expr += _scalar_from_symbol(arg, C)

            else:
                new_expr += _scalar_expr_from_mul(arg, C)
        new_expr = factor(new_expr)
        return factor_terms(new_expr, sign = True)

    else:
        return expr



def _symbol_from_mul(expr: Mul) -> Expr:
    if isinstance(expr, Number):
        return expr

    args = expr.args
    if isinstance(expr, Pow):
        return Symbol(str(args[0])[-1])**args[1]

    expr_has_coeff = isinstance(args[0], Number)
    variables = args[1:] if expr_has_coeff else args
    new_expr = args[0] if expr_has_coeff else S.One
    for var in variables:
        if isinstance(var, Pow):
            new_expr *= Symbol(str(var.args[0])[-1])**var.args[1]
        else:
            new_expr *= Symbol(str(var)[-1])
    return new_expr

def symbol_from_coord_scalar(expr: Expr) -> Expr:
    if (not hasattr(expr, "free_symbols") or
        not expr.free_symbols or
        not hasattr(next(iter(expr.free_symbols)), "system")):
        return expr

    expr = expand(expr)
    if isinstance(expr, BaseScalar):
        return Symbol(str(expr)[-1])

    elif isinstance(expr, (Mul, Pow)):
        return _symbol_from_mul(expr)

    elif isinstance(expr, Add):
        new_expr = S.Zero
        for arg in expr.args:
            if isinstance(arg, BaseScalar):
                new_expr += Symbol(str(arg)[-1])
            else:
                new_expr += _symbol_from_mul(arg)
        new_expr = factor(new_expr)
        return factor_terms(new_expr, sign = True)

    else:
        return expr