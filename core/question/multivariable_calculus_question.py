from abc import ABC
from sympy import Expr, latex
from pylatex.utils import NoEscape
from core.question import Question, register_question, register_type
from core.mathematics.multivariable_calculus import ScalarField, VectorField
from core.mathematics.geometry import Curve
from utilities.mathematics import awkward_number

@register_type()
class MultivariableCalculusQuestion(Question, ABC):

    name: tuple[str] = ("multivariable_calc", "Multivariable calculus")

    def __init__(
            self, topic: str,
            subtopic: str,
            **kwargs: bool
    ):
        super().__init__(topic, subtopic, **kwargs)


@register_question()
class LineIntegralQuestion(MultivariableCalculusQuestion):

    topic: tuple[str] = ("line_integral", "Line integrals")

    # TODO: Improve question LaTeX generation logic based on question subtopic etc.
    # TODO: Properly format answer LaTeX.

    """ subtopics: dict[str, str] = {
        "scalar_field": "Line integral of scalar fields",
        "vector_field": "Line integral of vector fields",
        "fundamental_theorem": "Fundamental theorem of line integrals",
        "conservative_vector_field": "Conservative vector fields",
        "green's_theorem": "Green's theorem"
    } """

    subtopics: dict[str, str] = {
        "scalar_field": "Line integrals of scalar fields",
        "vector_field": "Line integrals of vector fields",
        "fundamental_theorem": "Fundamental theorem of line integrals"
    }

    def __init__(self, subtopic, dimension = 3, curve_is_parametric = True, curve_is_implicit = False, **kwargs):
        super().__init__(self.topic[0], subtopic, **kwargs)

        self._dimension = dimension

        if subtopic not in self.subtopics:
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

class SurfaceIntegralQuestion(MultivariableCalculusQuestion):
    pass