from logging import info
from sympy import Expr, Symbol, factor_terms
from sympy.abc import t, theta
from sympy.vector import ParametricRegion
from core.regenerating import Regenerating
from utilities import ParametricRegionLatexPrinter
from utilities import (polynomial_from_coeffs, random_limits,
                                   random_weighted_coefficients)

# TODO: Write docstrings.
# TODO: Allow for curves to be geometric objects, e.g. triangles, circles etc.
# TODO: Allow for curves to be made piecewise.
# TODO: Implement wordy curve definitions.
# TODO: Implement implicit curve definitions.
# TODO: Complete docstring for the Curve class
class Curve(Regenerating):
    """

    Parameters
    ==========
    components: tuple[Expr], optional
        A tuple of expressions for manually defining a curve. Manual definitions should be used for
        testing only. The length of this tuple should match the ambient_dim, and only one symbol
        should be used. The symbol used in the expressions will override any symbols passed in the
        parameter argument.
    """

    def __init__(
            self,
            parameter: Symbol = t,
            ambient_dim: int = 3,
            linear_components: bool = False,
            components: tuple[Expr] = None,
            limits: tuple[int] = None
    ):
        self._parameter = parameter

        if ambient_dim not in (2, 3):
                msg = (f"Curve embedding into {ambient_dim}D space is not supported. "
                     "Ambient dimension should be 2 or 3.")
                raise ValueError(msg)
        self._ambient_dim: int = ambient_dim

        self._linear_components = linear_components

        self._manual_components = components
        self._manual_limis = limits

        self._regenerate()


    def _regenerate(self) -> None:
        if not self._manual_components:
            if not  self._manual_limis:
                self._curve: ParametricRegion = self._generate_random_parametric_curve(self._linear_components)
            else:
                self._curve: ParametricRegion = ParametricRegion(
                    self._generate_random_components(self._linear_components),
                    (self._parameter,) + self._manual_limis
                )
        else:
            if len(self._manual_components) not in (2, 3):
                msg = (f"Curve embedding into {len(self._manual_components)}D space is not supported. "
                     "Ambient dimension should be 2 or 3.")
                raise ValueError(msg)
            self._ambient_dim: int = len(self._manual_components)

            max_symbols: set[Symbol]
            max_len = 0
            for comp in self._manual_components:
                if not hasattr(comp, "free_symbols"):
                    continue

                elif len(comp.free_symbols) > max_len:
                    max_len = len(comp.free_symbols)
                    max_symbols = comp.free_symbols

            if max_len > 1:
                msg = (f" Parameters are {max_symbols}. Parametric curves can "
                    "only have one parameter. ")
                raise ValueError(msg)

            else:
                self._parameter: Symbol = next(iter(self._manual_components[0].free_symbols))

            lims = self._manual_limis if self._manual_limis else random_limits(-3, 3)
            self._curve: ParametricRegion = ParametricRegion(
                tuple(self._manual_components),
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
              f"with limits {self.curve.limits[self._parameter]}"))

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

    def _generate_random_polynomial(self, linear_components: bool) -> Expr:
        max_index = 2 if linear_components else 4
        index_weights = [1, 1] if linear_components else [0.5, 0.5, 1, 1]
        coeffs = random_weighted_coefficients(
            max_index = max_index,
            non_zero_coeffs_range = (1, 2),
            coeff_value_range = (-4, 4),
            non_zero_coeff_weights = [0.6, 0.4],
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09],
            index_weights = index_weights
        )
        return polynomial_from_coeffs(self.parameter, coeffs)

    def _generate_random_components(self, linear_components: bool) -> list[Expr]:
        return tuple([
            factor_terms(self._generate_random_polynomial(linear_components), sign = True)
            for _ in range(self._ambient_dim)
        ])

    def _generate_random_parametric_curve(self, linear_components: bool) -> ParametricRegion:
        return ParametricRegion(
            self._generate_random_components(linear_components),
            (self.parameter,) + random_limits(-3, 3)
        )

    def __repr__(self):
        return f"{self._curve}"