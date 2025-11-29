from abc import ABC
from sympy import Expr, latex
from pylatex.utils import NoEscape
from core.question.question import Question
from core.question.question_registry import register_question_type
from core.mathematics.multivariable_calculus import ScalarField, VectorField
from core.mathematics.geometry import Curve
from utilities.mathematics import awkward_number

class MultivariableCalculusQuestion(Question):


    subtopics: dict[str, list[str]] = {
        "line_integrals": ["scalar_field", "vector_field", "fundamental_theorem_of_line_integrals",
                          "conservative_vector_field", "green's_theorem"],
        "surface_integrals": ["scalar_field", "vector_field", "stoke's_theorem", "divergence_theorem"]
    }

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
            if subtopic not in ("vector_field", "scalar_field",
                                "fundamental_theorem_of_line_integrals"):
                msg = (f"{subtopic} is not a valid subtopic for the "
                       "line_integral question topic")
                raise ValueError(msg)

            field: VectorField | ScalarField = (
                    VectorField("F", dimension) if subtopic == "vector_field"
                    else ScalarField("phi", dimension)
            )
            linear_components = subtopic == "scalar_field"
            curve: Curve = Curve(ambient_dim = dimension, linear_components = linear_components)

            answer: Expr = field.calculate_line_integral(curve.curve)
            answer_is_awkward = awkward_number(answer)

            while answer_is_awkward:
                field.regenerate()
                curve.regenerate()

                answer = field.calculate_line_integral(curve.curve)
                answer_is_awkward = awkward_number(answer)

        self._answer: str = self._generate_answer_latex(answer)
        self._question: str = self._generate_question_latex(field, curve)

    @staticmethod
    def _generate_question_latex(vector_field: VectorField, curve: Curve) -> str:
        return NoEscape(
            rf"Let ${vector_field.name_latex}$ be the "
            f"vector field {vector_field.field_latex} and $C$ the "
            f"curve given by {curve.curve_latex}. "
            r"Calculate $\displaystyle\int_C"
            rf"{vector_field.name_latex}\cdot\mathbf{{dr}}$."
        )

    @staticmethod
    def _generate_answer_latex(answer: str) -> str:
        return NoEscape(f"${latex(answer)}$")


class LineIntegralQuestion(MultivariableCalculusQuestion):

    subtopics: list[str] = [
        "scalar_field", "vector_field", "fundamental_theorem_of_line_integrals",
        "conservative_vector_field", "green's_theorem"
    ]

    def __init__(self, subtopic, dimension = 3, curve_is_parametric = True, curve_is_implicit = False, **kwargs):
        super().__init__("line_integral", subtopic, dimension, curve_is_parametric, curve_is_implicit, **kwargs)

class SurfaceIntegralQuestion(MultivariableCalculusQuestion):
    pass