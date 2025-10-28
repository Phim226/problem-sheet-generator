import logging
from sympy import Expr, Symbol, latex
from sympy.abc import t, theta
from sympy.vector import ParametricRegion
from utilities.latex_formatting import format_component_latex, format_vector_function_latex
from utilities.mathematics import build_polynomial_from_coeffs, generate_non_zero_weighted_coefficients

# TODO: Allow for curves to be geometric objects, e.g. triangles, circles etc
# TODO: Detect if curve is closed
# TODO: Implement random curve limit generation
# TODO: Allow for curves to be made piecewise
# TODO: Implement wordy curve definitions
# TODO: Implement implicit curve definitions
class Curve():

    I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
    J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
    K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"

    def __init__(self, p: Symbol, dimension: int):

        if dimension not in (2, 3):
            raise ValueError((f"{dimension} is not a valid dimension. "
                            "It should be 2 or 3.")
                    )
        self._dimension = dimension

        self._curve = self._generate_random_parametric_curve(p, dimension)
        self._curve_latex = self._format_curve_latex(self._curve)

        logging.info(f"Curve is {self.curve.definition} with limits {self.curve.limits[p]}")

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
    def _generate_random_polynomial(p: Symbol) -> Expr:
        coeffs = generate_non_zero_weighted_coefficients(
            max_index = 4,
            non_zero_coeffs_range = (1, 2),
            coeff_value_range = (-4, 4),
            non_zero_coeff_weights = [0.6, 0.4],
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09],
            index_weights = [0.5, 0.5, 1, 1]
        )
        return build_polynomial_from_coeffs(p, coeffs)

    def _generate_random_parametric_curve(
            self,
            p: Symbol,
            dimension: int) -> ParametricRegion:
        x_component: Expr = self._generate_random_polynomial(p)
        y_component: Expr = self._generate_random_polynomial(p)
        z_component: Expr = (
            self._generate_random_polynomial(p) if dimension == 3 else 0
            )
        return ParametricRegion((x_component,
                                 y_component,
                                 z_component),
                                (p, 0, 1)
                )


    def _format_curve_latex(self, curve: ParametricRegion) -> str:
        curve_def_x: str = format_component_latex(curve.definition[0], is_x_component = True)
        curve_def_y: str = format_component_latex(curve.definition[1])
        curve_def_z: str = format_component_latex(curve.definition[2])

        curve_latex = format_vector_function_latex(
            curve_def_x,
            curve_def_y,
            curve_def_z
        )

        curve_lower_lim: int = curve.limits[t][0]
        curve_upper_lim: int = curve.limits[t][1]

        return (rf"$\mathbf{{r}}(t)={curve_latex}$ "
                rf"for ${curve_lower_lim}\le t\le {curve_upper_lim}$")