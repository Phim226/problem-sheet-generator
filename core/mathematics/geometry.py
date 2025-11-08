from logging import info
from sympy import Expr, Symbol, factor_terms
from sympy.abc import t, theta
from sympy.vector import ParametricRegion
from utilities.latex_formatting import ParametricRegionLatexPrinter
from utilities.mathematics import (polynomial_from_coeffs, random_limits,
                                   random_weighted_coefficients)

# TODO: Write docstrings.
# TODO: Allow for curves to be geometric objects, e.g. triangles, circles etc.
# TODO: Allow for curves to be made piecewise.
# TODO: Implement wordy curve definitions.
# TODO: Implement implicit curve definitions.
class Curve():


    def __init__(
            self,
            parameter: Symbol = t,
            ambient_dim: int = 3,
            components: tuple[Expr] = None,
            limits: tuple[int] = None
    ):
        if not components:
            self._parameter: Symbol = parameter

            if ambient_dim not in (2, 3):
                msg = (f"Curve embedding into {ambient_dim}D space is not supported. "
                     "Ambient dimension should be 2 or 3.")
                raise ValueError(msg)
            self._ambient_dim: int = ambient_dim

            if not limits:
                self._curve: ParametricRegion = self._generate_random_parametric_curve()
            else:
                self._curve: ParametricRegion = ParametricRegion(
                    self._generate_random_components(),
                    (self._parameter,) + limits
                )
        else:
            if len(components) not in (2, 3):
                msg = (f"Curve embedding into {len(components)}D space is not supported. "
                     "Ambient dimension should be 2 or 3.")
                raise ValueError(msg)
            self._ambient_dim: int = len(components)

            max_symbols: set[Symbol]
            max_len = 0
            for comp in components:
                if not hasattr(comp, "free_symbols"):
                    continue

                elif len(comp.free_symbols) > max_len:
                    max_len = len(comp.free_symbols)
                    max_symbols = comp.free_symbols

            if max_len == 0:
                self._parameter: Symbol = parameter

            elif max_len > 1:
                msg = (f" Parameters are {max_symbols}. Parametric curves can "
                    "only have one parameter. ")
                raise ValueError(msg)

            else:
                self._parameter: Symbol = next(iter(components[0].free_symbols))

            lims = limits if limits else random_limits(-3, 3)
            self._curve: ParametricRegion = ParametricRegion(
                tuple(components),
                (self._parameter,) + lims
            )

        printer: ParametricRegionLatexPrinter = ParametricRegionLatexPrinter()
        self._curve_latex: str = printer.parametric_curve_print(self)

        self.is_closed = (
            self._curve.definition.subs(
                self._parameter,
                self._curve.limits[self._parameter][0]
            )
            ==
            self._curve.definition.subs(
                self._parameter,
                self._curve.limits[self._parameter][1]
            )
        )

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

    def _generate_random_polynomial(self) -> Expr:
        coeffs = random_weighted_coefficients(
            max_index = 4,
            non_zero_coeffs_range = (1, 2),
            coeff_value_range = (-4, 4),
            non_zero_coeff_weights = [0.6, 0.4],
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09],
            index_weights = [0.5, 0.5, 1, 1]
        )
        return polynomial_from_coeffs(self.parameter, coeffs)

    def _generate_random_components(self) -> list[Expr]:
        return tuple([
            factor_terms(self._generate_random_polynomial(), sign = True)
            for _ in range(self._ambient_dim)
        ])

    def _generate_random_parametric_curve(self) -> ParametricRegion:
        return ParametricRegion(
            self._generate_random_components(),
            (self.parameter,) + random_limits(-3, 3)
        )