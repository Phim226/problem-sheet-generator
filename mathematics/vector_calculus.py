from abc import abstractmethod
from random import choices, random
from sympy import Add, Expr, S, factor, latex
from sympy.vector import CoordSys3D, ParametricRegion, Vector, vector_integrate
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

    # TODO: Make the random generation process more sophisticated
    @staticmethod
    def _generate_random_component(dimension: int, C: CoordSys3D, allow_zero: bool = True) -> Expr:
        """
        Generate weighted random coefficients for a polynomial field component.

        This function generates weighted random coefficients for the polynomial
        (c_0x^2 + c_1x + c_2)(c_3y^2 + c_4y + c_5)(c_6z^2 + c_7z + c_8) and then
        evaluates the product. This produces a polynomial in x, y and z of max
        total degree 6, consisting of 26 possible combinations of the multivariate
        monomial (x^n)(y^m)(z^t) with 0<=n,m,t<=2, plus a possible constant
        term. If the dimension is 2, no values are generated for c_6, c_7 and c_8.
        1% of the time the function will return 0.

        We first set all coefficients to be 0 and then randomly choose at most four
        to be non-zero. The selection of the number of coefficients is weighted.
        For the weighting [0.6, 0.3, 0.07, 0.03] this produces one non-zero
        coefficient 60% of the time, two 30% of the time and so on. This weighting
        makes simpler expressions more likely to be generated.

        The value of the coefficients is also weighted. A weighting
        [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09] for the possible values
        [-4, -3, -2, -1, 1, 2, 3, 4] produces -1 10% of the time, 1 40% of the time,
        -2 5%, 2 20% and so on.

        Note
        ----
        If the number of coefficients or the range of possible coefficient values is
        changed then the weightings should be changed accordingly as well. Otherwise
        you might get a ValueError if the number of weights doesn't match.
        """

        if allow_zero:
            return_zero: bool = random() < 0.05
            if return_zero:
                return S.Zero

        """ max_index: int = 3*dimension
        coeffs: list[int] = [0]*max_index

        min_num_non_zero = 1
        max_num_non_zero = 4
        number_of_coeffs: int = choices(
            population = range(min_num_non_zero, max_num_non_zero + 1),
            weights = [0.6, 0.3, 0.07, 0.03]
        )[0]

        smallest_coeff_value = -4
        highest_coeff_value = 4
        coeff_range: list[int] = list(range(
            smallest_coeff_value,
            highest_coeff_value + 1
            )
        )
        coeff_range.remove(0)

        index_range: list[int] = list(range(max_index))

        for _ in range(number_of_coeffs):
            index: int = choices(population = index_range)[0]
            index_range.remove(index)
            coeffs[index] = choices(
                population = coeff_range,
                weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09]
            )[0] """

        coeffs: list[int] = generate_non_zero_weighted_coefficients(
            max_index = 3*dimension,
            non_zero_coeffs_range = (1, 4),
            non_zero_coeff_weights = [0.6, 0.3, 0.07, 0.03],
            coeff_value_range = (-4, 4),
            coeff_value_weights = [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09]
        )
        x_coeffs: list[int] = coeffs[0:3]
        y_coeffs: list[int] = coeffs[3:6]
        z_coeffs: list[int] = coeffs[6:9] if dimension == 3 else None

        component_x_terms: Expr = (
            1 if all(c == 0 for c in x_coeffs)
            else build_polynomial_from_coeffs(C.x, x_coeffs)
        )
        component_y_terms: Expr = (
            1 if all(c == 0 for c in y_coeffs)
            else build_polynomial_from_coeffs(C.y, y_coeffs)
        )
        component_z_terms: Expr = (
            1 if not z_coeffs or all(c == 0 for c in z_coeffs)
            else build_polynomial_from_coeffs(C.z, z_coeffs)
        )

        return component_x_terms*component_y_terms*component_z_terms

class ScalarField(Field):


    def __init__(self, dimension: int):
        super().__init__(dimension)
        self._field: Expr = self._generate_random_component(dimension, self._C, allow_zero = False)


class VectorField(Field):


    I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
    J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
    K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"
    VECTOR_FIELD_SYMBOL_LATEX = r"\mathbf{{F}}"

    def __init__(self, dimension: int):
        super().__init__(dimension)

        all_components_zero = True
        while all_components_zero:

            self._x_component: Expr = factor(
                self._generate_random_component(dimension, self._C)
            )
            self._y_component: Expr = factor(
                self._generate_random_component(dimension, self._C)
            )
            self._z_component: Expr = factor(
                self._generate_random_component(dimension, self._C)
            )

            all_components_zero = (
                    (self._x_component is S.Zero) and
                    (self._y_component is S.Zero) and
                    (dimension == 2 or self._z_component is S.Zero)
            )



        C: CoordSys3D = CoordSys3D("C")
        self._field: Vector = self._x_component*C.i + self._y_component*C.j

        x_component_latex = self._format_component_latex(self._x_component)
        y_component_latex = self._format_component_latex(self._y_component)
        z_component_latex = None

        if dimension == 3:
            self._field += self._z_component*C.k

            z_component_latex = self._format_component_latex(
                self._z_component
            )

        self._field_latex: str = self._format_vector_field_latex(x_component_latex,
                                                                 y_component_latex,
                                                                 z_component_latex)

    @staticmethod
    def _normalise_component_latex(component_latex: str) -> str:
        latex_replacements: dict[str, str] = {
            "_{C}": "",
            r"\mathbf{{x}}": "x",
            r"\mathbf{{y}}": "y",
            r"\mathbf{{z}}": "z"
        }
        for latex, replacement_latex in latex_replacements.items():
            component_latex = component_latex.replace(latex, replacement_latex)
        return component_latex

    def _format_component_latex(self, component: Expr) -> str:
        """
        Format the latex for a component of the vector field.

        If the component is 1 or -1 then we return "" and "-" respectively,
        otherwise we would end up with a string -1i or 1i for example.

        If the component is an additive expression, such as x + 1, then
        we put brackets around it so that the final string is (x + 1)i.
        """

        if component is S.NegativeOne:
            return "-"
        if component is S.One:
            return ""
        if isinstance(component, Add):
            return rf"\left({self._normalise_component_latex(latex(component))}\right)"
        return self._normalise_component_latex(latex(component))

    def _format_vector_field_latex(
            self,
            x_latex: str,
            y_latex: str,
            z_latex: str
    ) -> str:
        """
        Format the LaTeX for the vector field expression.

        First the x and y component are built, then the z is appended if the
        dimension is 3. Since each component is connected by a + sign and
        occasionally components will be negative we could end up with a string
        such as +-2xj. So we replace all these instances with a - sign.

        Finally F(x, y, z) or F(x, y) is attached to the start of the string
        depending on the dimension (z_latex will be None if dimension is 2).
        """

        field_latex: str = (
            f"{x_latex}{self.I_HAT_LATEX}"
            f"+{y_latex}{self.J_HAT_LATEX}"
        )
        if z_latex:
            field_latex = f"{field_latex}+{z_latex}{self.K_HAT_LATEX}"

        # Clean up any leading minus signs.
        field_latex = field_latex.replace("+-", "-")

        field_latex = (
            f"{self.VECTOR_FIELD_SYMBOL_LATEX}"
            f"{"(x, y, z)" if z_latex else "(x, y)"}"
            f"={field_latex}"
        )

        return f"${field_latex}$"

    def calculate_line_integral(self, curve: ParametricRegion):
        return vector_integrate(self.field, curve)
