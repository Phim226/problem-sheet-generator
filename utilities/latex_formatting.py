from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.mathematics.multivariable_calculus import VectorField, ScalarField
    from core.mathematics.geometry import Curve
from logging import info
from sympy import Add, Expr, Mul, Number, Pow, Symbol, S, expand, factor_terms, latex
from sympy.printing.latex import LatexPrinter
from sympy.vector import BaseScalar, BaseVector, CoordSys3D, ParametricRegion, Vector, VectorZero
from sympy.vector.basisdependent import BasisDependent

# TODO: Write docstrings
class CleanVectorLatexPrinter(LatexPrinter):

    def vector_field_print(self, field: VectorField) -> str:
        return (rf"${field.name_latex}"
                f"(x, y{", z" if field.dimension == 3 else ""})="
                f"{self.doprint(field.field)}$")

    def scalar_field_print(self, field: ScalarField) -> str:
        return (f"${field.name_latex}"
                f"(x, y{", z" if field.dimension == 3 else ""})="
                f"{self._symbol_from_coord_scalar(field.field)}$")

    @staticmethod
    def _symbol_from_Mul(expr: Mul) -> Expr:
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

    def _symbol_from_coord_scalar(self, expr: Expr) -> Expr:
        if (not expr.free_symbols or
            not hasattr(next(iter(expr.free_symbols)), "system")):
            return expr

        expr = expand(expr)
        if isinstance(expr, BaseScalar):
            return Symbol(str(expr)[-1])

        elif isinstance(expr, (Mul, Pow)):
            return self._symbol_from_Mul(expr)

        elif isinstance(expr, Add):
            new_expr = S.Zero
            for arg in expr.args:
                if isinstance(arg, BaseScalar):
                    new_expr += Symbol(str(arg)[-1])
                else:
                    new_expr += self._symbol_from_Mul(arg)
            return factor_terms(new_expr, sign = True)

        else:
            return expr

    @staticmethod
    def _clean_base_vector_latex(vect: BaseVector) -> str:
        return latex(vect).replace(f"_{{{str(vect.system)}}}", "")

    def _print_BasisDependent(self, expr: BasisDependent) -> str:
        o1: list[str] = []
        if expr == expr.zero:
            return expr.zero._latex_form
        if isinstance(expr, Vector):
            items = expr.separate().items()
        else:
            items = [(0, expr)]

        for system, vect in items:
            inneritems = list(vect.components.items())
            inneritems.sort(key=lambda x: x[0].__str__())
            for base_vect, comp in inneritems:
                if comp == 1:
                    o1.append(f"+{self._clean_base_vector_latex(base_vect)}")
                elif comp == -1:
                    o1.append(f"-{self._clean_base_vector_latex(base_vect)}")
                else:
                    scalar_symbols = self._symbol_from_coord_scalar(comp)
                    arg_str = (
                        rf"\left({self._print(scalar_symbols)}\right)"
                        if isinstance(scalar_symbols, Add)
                        else self._print(scalar_symbols)
                    )
                    o1.append(
                        (f"{"" if arg_str[0] == "-" else "+"}"
                         f"{arg_str}"
                         f"{self._clean_base_vector_latex(base_vect)}")
                    )

        outstr = ("".join(o1))
        if outstr[0] == "+":
            outstr = outstr[1:]
        return outstr

# TODO: Maybe expand scope of class to ImplicitRegion and other geometric objects as well.
class ParametricRegionLatexPrinter(CleanVectorLatexPrinter):

    def parametric_curve_print(self, curve: Curve):
        parameter: Symbol = curve.parameter
        limits: list[int] = curve.curve.limits[parameter]
        return (rf"$\mathbf{{r}}({parameter})={self.doprint(curve.curve)}$ "
                rf"for ${limits[0]}\le {parameter}\le {limits[1]}$")

    def _print_ParametricRegion(self, region: ParametricRegion):
        C = CoordSys3D("C")
        curve_vect_defn: Vector = sum(
            (comp*vect for comp, vect in zip(region.definition, C.base_vectors())),
            VectorZero()
        )

        return self.doprint(curve_vect_defn)

