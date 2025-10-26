from abc import ABC, abstractmethod
from sympy.abc import t
from sympy.vector import CoordSys3D, Vector
from pylatex.utils import NoEscape
from question.question_registry import register_question_type
from mathematics.vector_calculus import VectorField
from mathematics.geometry import Curve

# TODO: Populate file with question classes

class Question(ABC):


    def __init__(self, topic: str, nested: bool = False, difficulty: str = "easy"):
        self._topic: str = topic
        self._nested: bool = nested
        self._difficulty: str = difficulty

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


    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    # TODO: Improve question latex generation logic based on question subtopic etc
    def __init__(self, topic: str, subtopic: str = "", dimension: int = 3, curve_is_parametric: bool = True, curve_is_implicit: bool = False):
        super().__init__(topic)
        self._dimension = dimension
        C = CoordSys3D("C")
        self._curve = Curve(t, dimension)
        self._vector_field = VectorField(dimension)
        self._vector_field_expression: Vector = self._vector_field.field
        self._field_latex: str = self._vector_field.field_latex
        print(f"Vector field expression: {self._vector_field_expression}")

    def generate_question_latex(self) -> str:
        return NoEscape(rf"Let ${self.VECTOR_FIELD_SYMBOL_LATEX}$ be the vector field {self._field_latex} and $C$ the curve given by {self._curve.curve_latex}. "\
                        rf"Calculate $\displaystyle\int_C{self.VECTOR_FIELD_SYMBOL_LATEX}\cdot\mathbf{{dr}}$.")

    def generate_answer(self):
        return self._vector_field.calculate_line_integral(self._curve.curve)