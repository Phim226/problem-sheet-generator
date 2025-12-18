from sympy import expand, factor, factor_terms, S
from sympy.abc import x, y, z
from sympy.vector import CoordSys3D
from problem_sheet_generator.utilities import scalar_expr_from_expr, symbol_from_coord_scalar
from problem_sheet_generator.utilities.symbol_manipulation import _scalar_from_symbol, _scalar_expr_from_mul, _symbol_from_mul

C = CoordSys3D("C")

scalar_sanity_cases = {
    C.x: C.x,
    C.y: C.y,
    C.z: C.z,
    C.x + C.y: C.x + C.y,
    C.x*(C.x + C.y): C.x*(C.x + C.y),
    C.x**2: C.x**2
}

constant_sanity_cases = {
    1: 1,
    0: 0,
    -1: -1,
    S.One: S.One,
    S.Zero: S.Zero,
    S.NegativeOne: S.NegativeOne
}

symbol_sanity_cases = {
    x: x,
    y: y,
    z: z,
    x + y: x + y,
    x*(x + y): x*(x + y),
    x**2: x**2
}

scalar_from_sym_test_cases = {
        x: C.x,
        y: C.y,
        z: C.z
}

scalar_from_mul_test_cases = {
    2*x: 2*C.x,
    2*y: 2*C.y,
    2*z: 2*C.z,
    -z: -C.z,
    x*y: C.x*C.y,
    3*x*z: 3*C.x*C.z,
    y*z: C.y*C.z,
    -2*x*y*z: -2*C.x*C.y*C.z,
    x**2: C.x**2,
    y**2: C.y**2,
    12392*z**2: 12392*C.z**2,
    x*y**2: C.x*C.y**2,
    x*x*x*x*x*x*x*x*x: C.x**9
}

scalar_expr_from_exp_test_cases = {
    x + x: 2*C.x,
    x + y: C.x + C.y,
    x - y: C.x - C.y,
    -3*z**2 + x*y: -3*C.z**2 + C.x*C.y,
    x*(x + y): C.x*(C.x + C.y),
    (x**2 + y**2*z)*(z**2 - 3*y): (C.x**2 + C.y**2*C.z)*(C.z**2 - 3*C.y)
}

def test_scalar_from_symbol(subtests):
    test_cases = scalar_from_sym_test_cases

    for i, (symbol, scalar) in enumerate(test_cases.items()):
        with subtests.test("Scalar test", i = i):
            assert _scalar_from_symbol(symbol, C) == scalar

def test_scalar_from_mul(subtests):
    test_cases = scalar_from_mul_test_cases

    for i, (mul_expr, scalar_expr) in enumerate(test_cases.items()):
        with subtests.test("Scalar test", i = i):
            assert _scalar_expr_from_mul(mul_expr, C) == scalar_expr

def test_scalar_expr_from_expr(subtests):
    test_cases = (scalar_sanity_cases | constant_sanity_cases | scalar_from_sym_test_cases |
                  scalar_from_sym_test_cases | scalar_expr_from_exp_test_cases)

    for i, (expr, scalar_expr) in enumerate(test_cases.items()):
        with subtests.test("Scalar test", i = i):
            assert scalar_expr_from_expr(expr, C) == factor_terms(factor(expand(scalar_expr)))

def test_symbol_from_mul(subtests):
    test_cases = {value: key for key, value in scalar_from_mul_test_cases.items()}

    for i, (scalar_expr, mul_expr) in enumerate(test_cases.items()):
        with subtests.test("Scalar test", i = i):
            assert _symbol_from_mul(scalar_expr) == mul_expr

def test_symbol_from_coord_scalar(subtests):
    inv_test_cases = scalar_from_sym_test_cases | scalar_from_sym_test_cases | scalar_expr_from_exp_test_cases

    symbol_cases = {value: key for key, value in inv_test_cases.items()}

    test_cases = symbol_sanity_cases | constant_sanity_cases | symbol_cases

    for i, (scalar_expr, expr) in enumerate(test_cases.items()):
        with subtests.test("Scalar test", i = i):
            assert symbol_from_coord_scalar(scalar_expr) == factor_terms(factor(expand(expr)))