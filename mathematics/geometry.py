from sympy import Symbol, latex
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

    def __init__(self, p: Symbol):
        self._curve = ParametricRegion((p, p, 2*p**2), (p, 0, 1))
        self._curve_latex = self._format_curve_latex(self._curve)
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