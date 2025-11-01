from logging import info
from abc import abstractmethod
from random import random
from sympy import (Expr,
                   S,
                   factor_terms)
from sympy.vector import (CoordSys3D, ParametricRegion, Vector,
                          vector_integrate)
from utilities.latex_formatting import CleanVectorLatexPrinter
from utilities.mathematics import (polynomial_from_coeffs,
                                   random_weighted_coefficients)

class Field():


    @abstractmethod
    def __init__(self, name: str, dimension: int):

        self._name = name

        if dimension not in (2, 3):
            raise ValueError((f"{dimension} is not a valid dimension. "
                            "Fields should have dimension 2 or 3.")
                    )
        self._dimension = dimension
        self._C = CoordSys3D("C")

    @property
    def name(self) -> str:
        return self._name

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def field(self) -> Expr | Vector:
        return self._field

    @property
    def field_latex(self) -> str:
        return self._field_latex

    # TODO: Change weights depending on whether field is vector or scalar
    def _generate_random_component(self, allow_zero: bool = True) -> Expr:
        if allow_zero:
            return_zero: bool = random() < 0.05
            if return_zero:
                return S.Zero

        # These index weights will favour smaller degree expressions
        index_weights = [0.5, 1, 1, 0.5, 1, 1]
        if self._dimension == 3:
            index_weights += [0.5, 1, 1] # The weights for the z coefficient indices
        coeffs: list[int] = random_weighted_coefficients(
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
            else polynomial_from_coeffs(self._C.x, x_coeffs)
        )
        component_y_terms: Expr = (
            1 if all(c == 0 for c in y_coeffs)
            else polynomial_from_coeffs(self._C.y, y_coeffs)
        )
        component_z_terms: Expr = (
            1 if not z_coeffs or all(c == 0 for c in z_coeffs)
            else polynomial_from_coeffs(self._C.z, z_coeffs)
        )

        return component_x_terms*component_y_terms*component_z_terms

class ScalarField(Field):

    # TODO: Attempt to parse name string as greek letter for latex (phi being the main one) otherwise name is verbatim
    def __init__(self, name: str, dimension: int):
        super().__init__(name, dimension)
        self._field: Expr = self._generate_random_component(
            allow_zero = False
        )

class VectorField(Field):


    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    def __init__(self, name: str, dimension: int):
        super().__init__(name, dimension)

        all_components_zero = True
        while all_components_zero:
            self._x_component: Expr = factor_terms(
                self._generate_random_component(),
                sign = True
            )
            self._y_component: Expr = factor_terms(
                self._generate_random_component(),
                sign = True
            )
            self._z_component: Expr = factor_terms(
                self._generate_random_component(),
                sign = True
            ) if dimension == 3 else S.Zero

            all_components_zero = (
                    (self._x_component is S.Zero) and
                    (self._y_component is S.Zero) and
                    (self._z_component is S.Zero)
            )

        self._field: Vector = (self._x_component*self._C.i +
                               self._y_component*self._C.j +
                               self._z_component*self._C.k)
        info(f"Vector field expression: {self.field}")

        printer: CleanVectorLatexPrinter = CleanVectorLatexPrinter()
        self._field_latex: str = printer.vector_field_print(self)


    def calculate_line_integral(self, curve: ParametricRegion):
        return vector_integrate(self.field, curve)
