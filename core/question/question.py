import logging
from abc import ABC, abstractmethod
from sympy import Rational, latex
from sympy.abc import t
from pylatex.utils import NoEscape
from core.question.question_registry import register_question_type
from core.mathematics.vector_calculus import ScalarField, VectorField
from core.mathematics.geometry import Curve
from utilities.mathematics import clumsy_rational

# TODO: Populate file with question classes.
# TODO: Give option for answer to be worked.
# TODO: Populated question classes with dictionaries of topics and subtopics
@register_question_type("question")
class Question(ABC):

    subtopics: dict[str, list[str]] = {}

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
                                "fundamental_thm_line_integrals"):
                msg = (f"{subtopic} is not a valid subtopic for the "
                       "line_integral question topic")
                raise ValueError(msg)

            answer_is_clumsy = True
            while answer_is_clumsy:
                curve: Curve = Curve(ambient_dim = dimension)
                field: VectorField | ScalarField = (
                    VectorField("F", dimension) if subtopic == "vector_field"
                    else ScalarField("phi", dimension)
                )

                answer: Rational = field.calculate_line_integral(curve.curve)
                answer_is_clumsy = clumsy_rational(answer)

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

@register_question_type("linear_algebra")
class LinearAlgebraQuestion(Question):

    subtopics: dict[str, list[str]] = {
        "vectors": ["vector_operations"],
        "matrices": ["matrix_operations"]
    }

    def __init__(self, topic, nested = False, difficulty = "easy"):
        super().__init__(topic, nested, difficulty)

    def _generate_question_latex(self, *args, **kwargs):
        return super()._generate_question_latex(*args, **kwargs)

    def _generate_answer_latex(self, *args, **kwargs):
        return super()._generate_answer_latex(*args, **kwargs)

@register_question_type("differential_equations")
class DifferentialEquationQuestion(Question):

    subtopics: dict[str, list[str]] = {
        "ODEs": ["first_order", "second_order"]
    }

    def __init__(self, topic, nested = False, difficulty = "easy"):
        super().__init__(topic, nested, difficulty)

    def _generate_question_latex(self, *args, **kwargs):
        return super()._generate_question_latex(*args, **kwargs)

    def _generate_answer_latex(self, *args, **kwargs):
        return super()._generate_answer_latex(*args, **kwargs)

@register_question_type("complex_analysis")
class ComplexAnalysisQuestion(Question):

    subtopics: dict[str, list[str]] = {
        "complex_numbers": ["argand_diagrams"]
    }

    def __init__(self, topic, nested = False, difficulty = "easy"):
        super().__init__(topic, nested, difficulty)

    def _generate_question_latex(self, *args, **kwargs):
        return super()._generate_question_latex(*args, **kwargs)

    def _generate_answer_latex(self, *args, **kwargs):
        return super()._generate_answer_latex(*args, **kwargs)

@register_question_type("calculus")
class CalculusQuestion(Question):

    subtopics: dict[str, list[str]] = {
        "derivatives": ["quotient_rule", "chain_rule", "product_rule", "implicit_differentiation"],
        "integrals": ["indefinite", "definite", "substitution", "integration_by_parts"],
        "limits": ["basic_computation", "one_sided_limits", "lhospitals_rule"],
        "series": []
    }

    def __init__(self, topic, nested = False, difficulty = "easy"):
        super().__init__(topic, nested, difficulty)

    def _generate_question_latex(self, *args, **kwargs):
        return super()._generate_question_latex(*args, **kwargs)

    def _generate_answer_latex(self, *args, **kwargs):
        return super()._generate_answer_latex(*args, **kwargs)

@register_question_type("analytic_geometry")
class AnalyticGeometryQuestion(Question):

    subtopics: dict[str, list[str]] = {
        "lines": ["line_equation"],
        "planes": ["plane_equation"],
        "conics": ["circles", "ellipses", "parabolas", "hyperbolas"],
    }

    def __init__(self, topic, nested = False, difficulty = "easy"):
        super().__init__(topic, nested, difficulty)

    def _generate_question_latex(self, *args, **kwargs):
        return super()._generate_question_latex(*args, **kwargs)

    def _generate_answer_latex(self, *args, **kwargs):
        return super()._generate_answer_latex(*args, **kwargs)

@register_question_type("trigonometry")
class TrigonometryQuestion(Question):

    subtopics: dict[str, list[str]] = {
        "triangles": ["sine_rule", "cosine_rule"]
    }

    def __init__(self, topic, nested = False, difficulty = "easy"):
        super().__init__(topic, nested, difficulty)

    def _generate_question_latex(self, *args, **kwargs):
        return super()._generate_question_latex(*args, **kwargs)

    def _generate_answer_latex(self, *args, **kwargs):
        return super()._generate_answer_latex(*args, **kwargs)