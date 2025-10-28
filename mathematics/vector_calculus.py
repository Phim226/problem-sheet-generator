import logging
from abc import abstractmethod
from random import random
from sympy import Expr, S, factor
from sympy.vector import CoordSys3D, ParametricRegion, Vector, vector_integrate
from utilities.latex_formatting import format_component_latex, format_vector_function_latex
from utilities.mathematics import build_polynomial_from_coeffs, generate_non_zero_weighted_coefficients

class Field():


    @abstractmethod
    def __init__(self, dimension: int):

        if dimension not in (2, 3):
            raise ValueError((f"{dimension} is not a valid dimension. "
                            "Fields should have dimension 2 or 3.")
                    )
        self._dimension = dimension
        self._C = CoordSys3D("C")

    @property
    def field(self) -> Expr | Vector:
        return self._field

    @property
    def field_latex(self) -> str:
        return self._field_latex

    def _generate_random_component(self, allow_zero: bool = True) -> Expr:
        if allow_zero:
            return_zero: bool = random() < 0.05
            if return_zero:
                return S.Zero

        # These index weights will favour smaller degree expressions
        index_weights = [0.5, 1, 1, 0.5, 1, 1]
        if self._dimension == 3:
            index_weights += [0.5, 1, 1] # The weights for the z coefficient indices
        coeffs: list[int] = generate_non_zero_weighted_coefficients(
            max_index = 3*self._dimension,
            non_zero_coeffs_range = (1, 4),
            coeff_value_range = (-4, 4),
            non_zero_coeff_weights = [0.6, 0.3, 0.07, 0.03],
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09],
            index_weights = index_weights
        )
        x_coeffs: list[int] = coeffs[0:3]
        y_coeffs: list[int] = coeffs[3:6]
        z_coeffs: list[int] = coeffs[6:9] if self._dimension == 3 else None

        component_x_terms: Expr = (
            1 if all(c == 0 for c in x_coeffs)
            else build_polynomial_from_coeffs(self._C.x, x_coeffs)
        )
        component_y_terms: Expr = (
            1 if all(c == 0 for c in y_coeffs)
            else build_polynomial_from_coeffs(self._C.y, y_coeffs)
        )
        component_z_terms: Expr = (
            1 if not z_coeffs or all(c == 0 for c in z_coeffs)
            else build_polynomial_from_coeffs(self._C.z, z_coeffs)
        )

        return component_x_terms*component_y_terms*component_z_terms

class ScalarField(Field):


    def __init__(self, dimension: int):
        super().__init__(dimension)
        self._field: Expr = self._generate_random_component(allow_zero = False)


class VectorField(Field):

    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    def __init__(self, dimension: int):
        super().__init__(dimension)

        all_components_zero = True
        while all_components_zero:

            self._x_component: Expr = factor(
                self._generate_random_component()
            )
            self._y_component: Expr = factor(
                self._generate_random_component()
            )
            self._z_component: Expr = factor(
                self._generate_random_component()
            ) if dimension == 3 else S.Zero

            all_components_zero = (
                    (self._x_component is S.Zero) and
                    (self._y_component is S.Zero) and
                    (self._z_component is S.Zero)
            )

        self._field: Vector = (self._x_component*self._C.i +
                               self._y_component*self._C.j +
                               self._z_component*self._C.k)
        logging.info(f"Vector field expression: {self._field}")

        self._field_latex: str = self._format_vector_field_latex()

    @staticmethod
    def _remove_coordinate_latex(component_latex: str) -> str | None:
        if component_latex in ("-", "+", None):
            return component_latex
        latex_replacements: dict[str, str] = {
            "_{C}": "",
            r"\mathbf{{x}}": "x",
            r"\mathbf{{y}}": "y",
            r"\mathbf{{z}}": "z"
        }
        for latex, replacement_latex in latex_replacements.items():
            component_latex = component_latex.replace(latex, replacement_latex)
        return component_latex

    def _format_vector_field_latex(self) -> str:
        x_component_latex = self._remove_coordinate_latex(
            format_component_latex(self._x_component, is_x_component = True)
        )
        y_component_latex = self._remove_coordinate_latex(
            format_component_latex(self._y_component)
        )
        z_component_latex = self._remove_coordinate_latex(
            format_component_latex(self._z_component)
        )
        field_latex = format_vector_function_latex(x_component_latex,
                                                   y_component_latex,
                                                   z_component_latex)

        field_latex = (
            f"{self.VECTOR_FIELD_SYMBOL_LATEX}"
            f"{"(x, y, z)" if self._dimension == 3 else "(x, y)"}"
            f"={field_latex}"
        )

        return f"${field_latex}$"

    def calculate_line_integral(self, curve: ParametricRegion):
        return vector_integrate(self.field, curve)
