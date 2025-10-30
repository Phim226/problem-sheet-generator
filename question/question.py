import logging
from typing import Any
from abc import ABC, abstractmethod
from sympy import Rational
from sympy.abc import t
from sympy.vector import Vector
from pylatex.utils import NoEscape
from question.question_registry import register_question_type
from mathematics.vector_calculus import VectorField
from mathematics.geometry import Curve
from utilities.mathematics import clumsy_rational

# TODO: Populate file with question classes
@register_question_type("question")
class Question(ABC):


    def __init__(self, topic: str, nested: bool = False, difficulty: str = "easy"):
        self._topic: str = topic
        self._nested: bool = nested
        self._difficulty: str = difficulty

    @property
    def topic(self):
        return self._topic

    @property
    def answer(self):
        return self._answer

    @property
    def question_latex(self):
        return self._question_latex

@register_question_type("vector_calculus")
class VectorCalculusQuestion(Question):


    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    # TODO: Improve question LaTeX generation logic based on question subtopic etc.
    # TODO: Properly format answer LaTeX.
    def __init__(
            self, topic: str, subtopic: str = "",
            dimension: int = 3, curve_is_parametric: bool = True,
            curve_is_implicit: bool = False, **kwargs: bool):
        super().__init__(topic)
        self._dimension = dimension

        answer_is_clumsy = True
        while answer_is_clumsy:
            curve: Curve = Curve(t, dimension)
            vector_field: VectorField = VectorField(dimension)
            answer: Rational = vector_field.calculate_line_integral(curve.curve)
            answer_is_clumsy = clumsy_rational(answer)
        self._answer: Any = answer
        self._question_latex: str = self._generate_question_latex(vector_field, curve)

    def _generate_question_latex(self, vector_field: VectorField, curve: Curve) -> str:
        return NoEscape(
            rf"Let ${self.VECTOR_FIELD_SYMBOL_LATEX}$ be the "
            f"vector field {vector_field.field_latex} and $C$ the "
            f"curve given by {curve.curve_latex}. "
            r"Calculate $\displaystyle\int_C"
            rf"{self.VECTOR_FIELD_SYMBOL_LATEX}\cdot\mathbf{{dr}}$."
        )