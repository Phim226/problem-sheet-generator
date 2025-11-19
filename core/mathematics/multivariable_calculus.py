from abc import abstractmethod
from functools import reduce
from logging import info
from random import random
from sympy import Expr, S, factor_terms, latex
from sympy.vector import (BaseScalar, CoordSys3D, ParametricRegion, Vector, VectorZero,
                          vector_integrate)
from utilities.latex_formatting import CleanVectorLatexPrinter
from utilities.mathematics import polynomial_from_coeffs, random_weighted_coefficients


# TODO: Write docstrings.
# TODO: Allow for manual creation (for strictly testing purposes).
class Field():


    @abstractmethod
    def __init__(self, name: str, dimension: int):

        self._name = name

        if dimension not in (2, 3):
            msg = (f"{dimension} dimensional fields are not supported. "
                   "The dimension should be 2 or 3.")
            raise ValueError(msg)
        self._dimension = dimension
        self._C = CoordSys3D("C")

    @property
    def name(self) -> str:
        return self._name

    @property
    def name_latex(self) -> str:
        return self._name_latex

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def field(self) -> Expr:
        return self._field

    @property
    def field_latex(self) -> str:
        return self._field_latex

    def _generate_component_from_coeffs(
            self, x_coeffs: list[int], y_coeffs: list[int], z_coeffs: list[int] = None,
            gen_by_sum: bool = None
    ) -> Expr:
        def make_component_terms(scalar: BaseScalar, coeffs: list[int]) -> Expr:
            return (S.One if not coeffs or all(c == 0 for c in coeffs)
                    else polynomial_from_coeffs(scalar, coeffs))

        terms = [
            make_component_terms(self._C.x, x_coeffs),
            make_component_terms(self._C.y, y_coeffs)
        ]
        if self._dimension == 3:
            terms.append(make_component_terms(self._C.z, z_coeffs))

        if (gen_by_sum is None and random() < 0.5) or gen_by_sum:
            return sum((term for term in terms), S.Zero)
        else:
            return reduce(lambda a, b: a*b, terms, S.One)

    # TODO: Change weights depending on whether field is vector or scalar.
    # TODO: Improve generation process to include functions (sin, cos, e, log etc), rationals and fractional powers.
    def _generate_random_component(self, allow_zero: bool = True) -> Expr:
        if allow_zero and random() < 0.05:
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
        x_coeffs, y_coeffs, z_coeffs = (coeffs[0:3], coeffs[3:6],
                                        coeffs[6:9] if self._dimension == 3 else None)

        return self._generate_component_from_coeffs(x_coeffs, y_coeffs, z_coeffs)

    def calculate_line_integral(self, curve: ParametricRegion):
        return vector_integrate(self._field, curve)

    def __repr__(self):
        return f"{self._name} = {self._field}"

# TODO: Include validation of manual inputs in ScalarField and VectorField.
class ScalarField(Field):

    # TODO: Attempt to parse name string as greek letter for latex (phi being the main one) otherwise name is verbatim
    def __init__(
            self,
            name: str,
            dimension: int,
            component_coeffs: list[list[int]] = None,
            gen_by_sum: bool = None
    ):
        super().__init__(name, dimension)

        self._name_latex = latex(name)

        if component_coeffs:
            self._field: Expr = self._generate_component_from_coeffs(component_coeffs[0],
                                                                     component_coeffs[1],
                                                                     component_coeffs[2],
                                                                     gen_by_sum)

        else:
            self._field: Expr = self._generate_random_component(allow_zero = False)

class VectorField(Field):


    def __init__(
            self,
            name: str,
            dimension: int,
            component_coeffs: list[list[list[int]]] = None,
            gen_by_sum: bool = None
    ):
        super().__init__(name, dimension)

        self._name_latex = rf"\mathbf{{{latex(name)}}}"

        if component_coeffs:
            self._components: list[Expr] = [
                factor_terms(self._generate_component_from_coeffs(component_coeffs[i][0],
                                                                  component_coeffs[i][1],
                                                                  component_coeffs[i][2],
                                                                  gen_by_sum))
                for i in range(dimension)
            ]

        else:
            while True:
                self._components: list[Expr] = [
                    factor_terms(self._generate_random_component(), sign = True)
                    for _ in range(dimension)
                ]
                if not all(c is S.Zero for c in self._components):
                    break

        self._field: Vector = sum(
            (comp*vect for comp, vect in zip(self._components, self._C.base_vectors())),
            VectorZero()
        )

        info(f"Vector field expression: {self._field}")

        printer: CleanVectorLatexPrinter = CleanVectorLatexPrinter()
        self._field_latex: str = printer.vector_field_print(self)
