import logging
from abc import ABC, abstractmethod

# TODO: Populate file with question classes.
# TODO: Give option for answer to be worked.
# TODO: Populated question classes with dictionaries of topics and subtopics
class Question(ABC):

    subtopics: dict[str, list[str]] = {}

    def __init__(self, topic: str, subtopic: str, nested: bool = False, difficulty: str = "easy"):
        self._topic: str = topic
        self._subtopic: str = subtopic
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

""" @register_question_type("linear_algebra")
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
        return super()._generate_answer_latex(*args, **kwargs) """