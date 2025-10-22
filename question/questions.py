from abc import ABC, abstractmethod
from typing import Dict
import sympy as sp
from sympy.abc import t
from sympy.vector import Vector, CoordSys3D, ParametricRegion, vector_integrate
from pylatex.utils import NoEscape
from question.question_registry import register_question_type
from mathematics.vector_calculus import VectorField

class Question(ABC):
    def __init__(self, topic: str, nested: bool = False, difficulty: str = "easy"):
        self._topic = topic
        self._nested = nested
        self._difficulty = difficulty

    @property
    def topic(self):
        return self._topic

    @classmethod
    @abstractmethod
    def generate_question_latex(self):
        pass

    @abstractmethod
    def generate_answer(self):
        pass

@register_question_type("vector_calculus")
class VectorCalculusQuestion(Question):

    I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
    J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
    K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"
    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    def __init__(self, topic: str, subtopic: str = "", dimension: int = 3, curve_is_parametric: bool = True, curve_is_implicit: bool = False):
        super().__init__(topic)
        self._dimension = dimension
        C = CoordSys3D("C")
        self._curve = ParametricRegion((2*t, t, 2*t**2), (t, 0, 1))
        self._F: Vector = VectorField(dimension).field
        self._F: Vector = (1+C.x)*C.i + -2*C.y*C.j + C.z*C.k


    def _reformat_vector_field_latex(self, latex: str) -> str:
        vector_field_latex_dict: Dict[str, str] = {"_{C}": "", r"\mathbf{{x}}": "x", r"\mathbf{{y}}": "y", r"\mathbf{{z}}": "z", r"+ -": "-"}
        for unwanted_latex, replacement_latex in vector_field_latex_dict.items():
            latex = latex.replace(unwanted_latex, replacement_latex)
        return rf"${self.VECTOR_FIELD_SYMBOL_LATEX}{"(x, y, z)" if self._dimension == 3 else "(x, y)"}={latex}$"

    def _format_curve_latex(self, curve: ParametricRegion) -> str:
        curve_def_x: str = sp.latex(curve.definition[0])
        curve_def_y: str = sp.latex(curve.definition[1])
        curve_def_z: str = sp.latex(curve.definition[2])
        curve_lower_lim: int = curve.limits[t][0]
        curve_upper_lim: int = curve.limits[t][1]
        return rf"$\mathbf{{r}}(t)={curve_def_x}{self.I_HAT_LATEX}+{curve_def_y}{self.J_HAT_LATEX}+{curve_def_z}{self.K_HAT_LATEX}$ "\
            rf"for ${curve_lower_lim}\le t\le {curve_upper_lim}$"

    def generate_question_latex(self) -> str:
        vector_field_latex: str = self._reformat_vector_field_latex(sp.latex(self._F))
        curve_latex: str = self._format_curve_latex(self._curve)
        return NoEscape(rf"Let ${self.VECTOR_FIELD_SYMBOL_LATEX}$ be the vector field {vector_field_latex} and $C$ the curve given by {curve_latex}. "\
                        rf"Calculate $\displaystyle\int_C{self.VECTOR_FIELD_SYMBOL_LATEX}\cdot\mathbf{{dr}}$.")

    def generate_answer(self):
        return super().generate_answer()