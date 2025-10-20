from abc import ABC, abstractmethod
from sympy.abc import t
from sympy.vector import CoordSys3D, ParametricRegion, vector_integrate
import sympy as sp
from pylatex.utils import NoEscape

QUESTION_REGISTRY = {}

def register_question_type(name: str):
    def wrapper(cls: type):
        QUESTION_REGISTRY[name] = cls
        return cls
    return wrapper

def create_question(name, topic, **kwargs):
    cls = QUESTION_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unkown question type: {name}")
    return cls(topic, **kwargs)

class Question(ABC):
    def __init__(self, topic: str):
        self._topic = topic

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
    VECT_FIELD_LATEX = r"\mathbf{{F}}"

    def __init__(self, topic):
        super().__init__(topic)

        C = CoordSys3D("C")
        self._curve = ParametricRegion((t, t, 2*t**2), (t, 0, 1))
        self._F = C.y*C.i + C.x*C.j + C.z*C.k

    def _reformat_vector_field_latex(self, latex: str):
        vector_field_latex_dic = {r"\left(": "", r"\right)": "", "_{C}": "", r"\mathbf{{x}}": "x", r"\mathbf{{y}}": "y", r"\mathbf{{z}}": "z",}
        for i, j in vector_field_latex_dic.items():
            latex = latex.replace(i, j)
        return rf"${self.VECT_FIELD_LATEX}(x, y, z)={latex}$"
    
    def _format_curve_latex(self, curve: ParametricRegion):
        curve_def_x = sp.latex(curve.definition[0])
        curve_def_y = sp.latex(curve.definition[1])
        curve_def_z = sp.latex(curve.definition[2])
        curve_lower_lim = curve.limits[t][0]
        curve_upper_lim = curve.limits[t][1]
        return rf"$\mathbf{{r}}(t)={curve_def_x}{self.I_HAT_LATEX}+{curve_def_y}{self.J_HAT_LATEX}+{curve_def_z}{self.K_HAT_LATEX}$ for ${curve_lower_lim}\le t\le {curve_upper_lim}$"

    def generate_question_latex(self):
        vector_field_latex = self._reformat_vector_field_latex(sp.latex(self._F))
        curve_latex = self._format_curve_latex(self._curve)
        return NoEscape(rf"Let ${self.VECT_FIELD_LATEX}$ be the vector field {vector_field_latex} and $C$ the curve given by {curve_latex}. Calculate $\displaystyle\int_C{self.VECT_FIELD_LATEX}\cdot\mathbf{{dr}}$.")
    
    def generate_answer(self):
        return super().generate_answer()