from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mathematics.vector_calculus import VectorField, ScalarField
    from mathematics.geometry import Curve
from logging import info
from sympy import (Add, Expr, Mul, Number, Pow, Symbol,
                   S,
                   expand, factor_terms, latex)
from sympy.printing.latex import LatexPrinter
from sympy.vector import (BaseScalar, BaseVector, CoordSys3D,
                          ParametricRegion, Vector, VectorZero)
from sympy.vector.basisdependent import BasisDependent

I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"

def format_vector_component_latex(
          component: Expr,
          is_x_component: bool = False
) -> str:
    """
    Format the latex for a component of the vector function.

    Parameters
    =========
    component: Expr
        The sympy expression object of the component being formatted.

    is_x_component: bool, optional
        If the component is the x component then no leading + sign is added.
        Default is False.

    Returns
    ======
    str
        The LaTeX string for the vector function component.
    """
    if component is S.NegativeOne:
        return "-"
    elif component is S.One:
        return "+"
    elif component is S.Zero:
        return None
    elif isinstance(component, Add):
        return rf"{"+"}\left({latex(component)}\right)"

    component_latex = latex(component)
    if is_x_component:
         return component_latex
    return f"{"+" + component_latex if component_latex[0] != "-" else component_latex}"

def format_vector_function_latex(
            x_latex: str,
            y_latex: str,
            z_latex: str
    ) -> str:
        """
        Format the LaTeX for a vector function expression.

        Parameters
        =========
        x_latex: str
            LaTeX for the x component of the vector function.

        y_latex: str
            LaTeX for the y component of the vector function.

        z_latex: str
            LaTeX for the z component of the vector function.

        Returns
        ======
        str
            The LaTeX of the vector function.
        """
        vector_latex: str = (
            f"{x_latex + I_HAT_LATEX if x_latex is not None else ""}"
            f"{y_latex + J_HAT_LATEX if y_latex is not None else ""}"
            f"{z_latex + K_HAT_LATEX if z_latex is not None else ""}"
        )

        if vector_latex[0] == "+":
            vector_latex = vector_latex[1:]

        return vector_latex


# TODO: Write docstrings
class CleanVectorLatexPrinter(LatexPrinter):

    def vector_field_print(self, field: VectorField) -> str:
        return (rf"${field.name_latex}"
                f"(x, y{", z" if field.dimension == 3 else ""})="
                f"{self.doprint(field.field)}$")

    def scalar_field_print(self, field: ScalarField) -> str:
        return (f"${field.name}"
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


# TODO: Integrate _print_ParametricRegion function into generation of curve latex.
# TODO: Maybe expand scope of class to ImplicitRegion and other geometric objects as well.
class ParametricRegionLatexPrinter(CleanVectorLatexPrinter):

    def parametric_curve_print(self, curve: Curve):
        pass

    def _print_ParametricRegion(self, region: ParametricRegion):
        C = CoordSys3D("C")
        curve_vect_defn: Vector = sum(
            (comp*vect for comp, vect in
             zip(region.definition, C.base_vectors())),
            VectorZero()
        )

        return self.doprint(curve_vect_defn)

