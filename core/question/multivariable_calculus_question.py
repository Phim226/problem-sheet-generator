from abc import ABC
from sympy import Expr, latex
from pylatex.utils import NoEscape
from core.question import Question, register_question, register_type
from core.mathematics.multivariable_calculus import ScalarField, VectorField, Field
from core.mathematics.geometry import Curve
from utilities import awkward_number

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
class IntegralTheoremsQuestion(MultivariableCalculusQuestion):

    topic: tuple[str] = ("integral_theorems", "Integral theorems")

    subtopics: dict[str, str] = {
        "greens_theorem": "Green's theorem"
    }

    def __init__(self, subtopic, dimension = 3, **kwargs):
        super().__init__(self.topic[0], subtopic, **kwargs)

        self._dimension = 2 if subtopic == 'greens_theorem' else dimension

        field: VectorField = VectorField("F", self._dimension)

        region: Curve = Curve(force_closed = subtopic == "greens_theorem")

        answer = field.calculate_line_integral(region)

        self._answer: str = self._generate_answer_latex(answer)
        self._question: str = self._generate_question_latex(field, region)

    def _generate_question_latex(self, field: Field, curve: Curve):
        vertices = curve.region.args
        setup_latex = (f"Let ${field.name_latex}$ be the vector field {field.field_latex} and "
                       f"$C$ the positively oriented triangle with vertices at ${tuple(vertices[0])}, "
                       f"{tuple(vertices[1])}$ and ${tuple(vertices[2])}$. ")


        question_latex = rf"Use Green's Theorem to calculate $\displaystyle\oint {field.name_latex}\cdot\mathbf{{dr}}$"

        return NoEscape(setup_latex + question_latex)

    @staticmethod
    def _generate_answer_latex(answer: str) -> str:
        return NoEscape(f"${latex(answer)}$")


@register_question()
class LineIntegralQuestion(MultivariableCalculusQuestion):

    topic: tuple[str] = ("line_integral", "Line integrals")

    # TODO: Improve question LaTeX generation logic based on question subtopic etc.
    # TODO: Properly format answer LaTeX.

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

        linear_components: bool = subtopic == "scalar_field"
        curve: Curve = Curve(ambient_dim = dimension, linear_components = linear_components)

        answer_func = field.calculate_line_integral if subtopic != "fundamental_theorem" else field.line_integral_via_fund_thm
        answer: Expr = answer_func(curve)

        answer_is_awkward = awkward_number(answer)

        while answer_is_awkward:
            field.regenerate()
            curve.regenerate()

            answer = answer_func(curve)
            answer_is_awkward = awkward_number(answer)

        self._answer: str = self._generate_answer_latex(answer)
        self._question: str = self._generate_question_latex(field, curve)

    def _generate_question_latex(self, field: Field, curve: Curve) -> str:
        setup_latex: str = (f"Let ${field.name_latex}$ be the "
            f"vector field {field.field_latex} and $C$ the "
            f"curve given by {curve.region_latex}. ")

        question_latex: str = (
            rf"Calculate $\displaystyle\int_C{r"\nabla" if self._subtopic == "fundamental_theorem" else ""}"
            rf"{field.name_latex}{r"\, ds" if self._subtopic == "scalar_field" else rf"\cdot\mathbf{{dr}}"}$."
        )

        return NoEscape(setup_latex + question_latex)

    @staticmethod
    def _generate_answer_latex(answer: str) -> str:
        return NoEscape(f"${latex(answer)}$")

class SurfaceIntegralQuestion(MultivariableCalculusQuestion):
    pass