from logging import info
from sympy import Expr, Symbol, factor_terms
from sympy.abc import t, theta
from sympy.vector import ParametricRegion
from utilities.latex_formatting import ParametricRegionLatexPrinter
from utilities.mathematics import (polynomial_from_coeffs,
                                   random_limits,
                                   random_weighted_coefficients)

# TODO: Allow for curves to be geometric objects, e.g. triangles, circles etc
# TODO: Detect if curve is closed
# TODO: Allow for curves to be made piecewise
# TODO: Implement wordy curve definitions
# TODO: Implement implicit curve definitions
class Curve():


    def __init__(self, parameter: Symbol, dimension: int):
        self._parameter: Symbol = parameter
        if dimension not in (2, 3):
            raise ValueError((f"{dimension} is not a valid dimension. "
                            "It should be 2 or 3.")
                    )
        self._dimension: int = dimension

        self._curve: ParametricRegion = self._generate_random_parametric_curve(
            parameter,
            dimension
        )

        printer: ParametricRegionLatexPrinter = ParametricRegionLatexPrinter()
        self._curve_latex: str = printer.parametric_curve_print(self)

        info((f"Curve is {self.curve.definition} "
              f"with limits {self.curve.limits[parameter]}"))

        """ if p is t:
            print(f"Symbol is {t}")
        elif p is theta:
            print(f"Symbol is {theta}") """

    @property
    def curve_latex(self) -> str:
        return self._curve_latex

    @property
    def curve(self) -> ParametricRegion:
        return self._curve

    @property
    def parameter(self) -> Symbol:
        return self._parameter

    @staticmethod
    def _generate_random_polynomial(parameter: Symbol) -> Expr:
        coeffs = random_weighted_coefficients(
            max_index = 4,
            non_zero_coeffs_range = (1, 2),
            coeff_value_range = (-4, 4),
            non_zero_coeff_weights = [0.6, 0.4],
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09],
            index_weights = [0.5, 0.5, 1, 1]
        )
        return polynomial_from_coeffs(parameter, coeffs)

    def _generate_random_parametric_curve(
            self,
            parameter: Symbol,
            dimension: int
    ) -> ParametricRegion:
        components = [
            factor_terms(
                self._generate_random_polynomial(parameter),
                sign = True
            )
            for _ in range(dimension)
        ]
        if dimension == 2:
            components.append(0)

        return ParametricRegion(
            tuple(components),
            (parameter,) + random_limits(-3, 3)
        )