import logging
from abc import ABC, abstractmethod
from sympy import Rational, latex
from sympy.abc import t
from pylatex.utils import NoEscape
from question.question_registry import register_question_type
from mathematics.vector_calculus import ScalarField, VectorField
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
    def topic(self) -> str:
        return self._topic

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def question(self) -> str:
        return self._question

    @abstractmethod
    def _generate_question_latex(self, *args, **kwargs):
        pass

    @abstractmethod
    def _generate_answer_latex(self, *args, **kwargs):
        pass



@register_question_type("vector_calculus")
class VectorCalculusQuestion(Question):


    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    # TODO: Improve question LaTeX generation logic based on question subtopic etc.
    # TODO: Properly format answer LaTeX.
    def __init__(
            self, topic: str,
            subtopic: str = "",
            dimension: int = 3,
            curve_is_parametric: bool = True,
            curve_is_implicit: bool = False,
            **kwargs: bool
    ):
        super().__init__(topic)
        self._dimension = dimension

        if topic == "line_integral":
            if subtopic not in ("vector_field",
                                "scalar_field",
                                "fundamental_thm_line_integrals"):
                msg = (f"{subtopic} is not a valid subtopic for the "
                       "line_integral topic")
                raise ValueError(msg)

            answer_is_clumsy = True
            while answer_is_clumsy:
                curve: Curve = Curve(t, dimension)
                field: VectorField | ScalarField = (
                    VectorField(dimension) if subtopic == "vector_field"
                    else ScalarField(dimension)
                )

                answer: Rational = field.calculate_line_integral(curve.curve)
                answer_is_clumsy = clumsy_rational(answer)
        self._answer: str = self._generate_answer_latex(answer)
        self._question: str = self._generate_question_latex(field, curve)

    def _generate_question_latex(self, vector_field: VectorField, curve: Curve) -> str:
        return NoEscape(
            rf"Let ${self.VECTOR_FIELD_SYMBOL_LATEX}$ be the "
            f"vector field {vector_field.field_latex} and $C$ the "
            f"curve given by {curve.curve_latex}. "
            r"Calculate $\displaystyle\int_C"
            rf"{self.VECTOR_FIELD_SYMBOL_LATEX}\cdot\mathbf{{dr}}$."
        )

    @staticmethod
    def _generate_answer_latex(answer: str) -> str:
        return NoEscape(f"${latex(answer)}$")