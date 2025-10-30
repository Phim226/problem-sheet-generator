import logging
from sympy import Expr, Symbol, factor_terms
from sympy.abc import t, theta
from sympy.vector import ParametricRegion
from utilities.latex_formatting import (format_component_latex,
                                        format_vector_function_latex)
from utilities.mathematics import (polynomial_from_coeffs,
                                   random_limits,
                                   random_weighted_coefficients)

# TODO: Allow for curves to be geometric objects, e.g. triangles, circles etc
# TODO: Detect if curve is closed
# TODO: Allow for curves to be made piecewise
# TODO: Implement wordy curve definitions
# TODO: Implement implicit curve definitions
class Curve():

    I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
    J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
    K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"

    def __init__(self, param: Symbol, dimension: int):
        self._param = param
        if dimension not in (2, 3):
            raise ValueError((f"{dimension} is not a valid dimension. "
                            "It should be 2 or 3.")
                    )
        self._dimension = dimension

        self._curve = self._generate_random_parametric_curve(param, dimension)
        self._curve_latex = self._format_curve_latex(self._curve)

        logging.info((f"Curve is {self.curve.definition} "
                      f"with limits {self.curve.limits[param]}"))

        """ if p is t:
            print(f"Symbol is {t}")
        elif p is theta:
            print(f"Symbol is {theta}") """

    @property
    def curve_latex(self):
        return self._curve_latex

    @property
    def curve(self):
        return self._curve

    @staticmethod
    def _generate_random_polynomial(param: Symbol) -> Expr:
        coeffs = random_weighted_coefficients(
            max_index = 4,
            non_zero_coeffs_range = (1, 2),
            coeff_value_range = (-4, 4),
            non_zero_coeff_weights = [0.6, 0.4],
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09],
            index_weights = [0.5, 0.5, 1, 1]
        )
        return polynomial_from_coeffs(param, coeffs)

    def _generate_random_parametric_curve(
            self,
            param: Symbol,
            dimension: int) -> ParametricRegion:
        x_component: Expr = factor_terms(
            self._generate_random_polynomial(param),
            sign = True
        )
        y_component: Expr = factor_terms(
            self._generate_random_polynomial(param),
            sign = True
        )
        z_component: Expr = factor_terms(
            self._generate_random_polynomial(param),
            sign = True
        ) if dimension == 3 else 0

        return ParametricRegion((x_component,
                                 y_component,
                                 z_component),
                                (param,) + random_limits(-3, 3)
                )


    def _format_curve_latex(self, curve: ParametricRegion) -> str:
        curve_def_x: str = format_component_latex(
            curve.definition[0],
            is_x_component = True
        )
        curve_def_y: str = format_component_latex(curve.definition[1])
        curve_def_z: str = format_component_latex(curve.definition[2])

        curve_latex = format_vector_function_latex(
            curve_def_x,
            curve_def_y,
            curve_def_z
        )

        lower_lim: int = curve.limits[self._param][0]
        upper_lim: int = curve.limits[self._param][1]

        return (rf"$\mathbf{{r}}({self._param})={curve_latex}$ "
                rf"for ${lower_lim}\le {self._param}\le {upper_lim}$")