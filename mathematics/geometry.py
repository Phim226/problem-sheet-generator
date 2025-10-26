from random import choices
from sympy import Expr, Symbol, latex
from sympy.abc import t, theta
from sympy.vector import ParametricRegion

# TODO: Allow for curves to be geometric objects, e.g. triangles, circles etc
# TODO: Detect if curve is closed
# TODO: Implement random curve generation
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

        self._curve = ParametricRegion((p, p, 2*p**2), (p, 0, 1))
        self._curve_latex = self._format_curve_latex(self._curve)
        print(self._generate_random_parametric_curve(p, dimension))

        if p is t:
            print(f"Symbol is {t}")
        elif p is theta:
            print(f"Symbol is {theta}")

    @property
    def curve_latex(self):
        return self._curve_latex

    @property
    def curve(self):
        return self._curve

    @staticmethod
    def _generate_random_polynomial(p: Symbol) -> Expr:
        coeffs = [0, 0, 0, 0]

        min_num_non_zero = 1
        max_num_non_zero = 2
        number_of_coeffs: int = choices(
            population = range(
                min_num_non_zero,
                max_num_non_zero + 1
            ),
            weights = [0.6, 0.4]
        )[0]

        smallest_coeff_value = -4
        highest_coeff_value = 4
        coeff_range: list[int] = list(range(
            smallest_coeff_value,
            highest_coeff_value + 1
            )
        )
        coeff_range.remove(0)

        index_range: list[int] = list(range(len(coeffs)))

        for _ in range(number_of_coeffs):
            index: int = choices(population = index_range)[0]
            index_range.remove(index)
            coeffs[index] = choices(
                population = coeff_range,
                weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09]
            )[0]

        return coeffs[0]*p**3 + coeffs[1]*p**2 + coeffs[2]*p + coeffs[3]

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
        curve_def_x: str = latex(curve.definition[0])
        curve_def_y: str = latex(curve.definition[1])
        curve_def_z: str = latex(curve.definition[2])

        curve_lower_lim: int = curve.limits[t][0]
        curve_upper_lim: int = curve.limits[t][1]

        return (rf"$\mathbf{{r}}(t)={curve_def_x}{self.I_HAT_LATEX}"
                rf"+{curve_def_y}{self.J_HAT_LATEX}"
                rf"+{curve_def_z}{self.K_HAT_LATEX}$ "
                rf"for ${curve_lower_lim}\le t\le {curve_upper_lim}$")