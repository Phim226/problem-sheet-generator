from abc import abstractmethod
from random import choices
from sympy import Expr, S
from sympy.abc import x, y, z
from sympy.vector import CoordSys3D, Vector

class Field():

    @abstractmethod
    def __init__(self, dimension: int):
        if dimension not in (2, 3):
            raise ValueError(f"{dimension} is not a valid dimension. Fields should have dimension 2 or 3.")
        self._dimension = dimension

    @property
    def field(self):
        return self._field


    def _generate_random_field_component(self, dimension: int) -> Expr:
        """
        Generate weighted random coefficients for a polynomial field component.

        This function generates weighted random coefficients for the polynomial
        (c_0x^2 + c_1x + c_2)(c_3y^2 + c_4y + c_5)(c_6z^2 + c_7z + c_8) and then
        evaluates the product. This produces a polynomial in x, y and z of max
        total degree 6, consisting of 26 possible combinations of the multivariate
        monomial (x^n)(y^m)(z^t) with 0<=n,m,t<=2, plus a possible constant
        term. If the dimension is 2, no values are generated for c_6, c_7 and c_8.

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

        max_index = 3*dimension
        coeffs: list[int] = [0]*max_index
        number_of_coeffs: int = choices(population= range(1, 5), weights = [0.6, 0.3, 0.07, 0.03])[0]
        coeff_range: list[int] = list(range(-4, 5))
        coeff_range.remove(0)
        index_range: list[int] = list(range(max_index))
        for _ in range(number_of_coeffs):
            index = choices(population=index_range)[0]
            index_range.remove(index)
            coeffs[index] = choices(population = coeff_range, weights =[0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09])[0]
        x_coeffs: list[int] = coeffs[0:3]
        y_coeffs: list[int] = coeffs[3:6]
        z_coeffs: list[int] = coeffs[6:9] if dimension == 3 else None
        component_x_terms: Expr = 1 if all(c==0 for c in x_coeffs) else x_coeffs[0]*x**2 + x_coeffs[1]*x + x_coeffs[2]
        component_y_terms: Expr = 1 if all(c==0 for c in y_coeffs) else y_coeffs[0]*y**2 + y_coeffs[1]*y + y_coeffs[2]
        component_z_terms: Expr = 1 if not z_coeffs or all(c==0 for c in z_coeffs) else z_coeffs[0]*z**2 + z_coeffs[1]*z + z_coeffs[2]
        return component_x_terms*component_y_terms*component_z_terms

class ScalarField(Field):

    def __init__(self, dimension: int):
        super().__init__(dimension)
        self._field = self._generate_random_field_component(dimension)


class VectorField(Field):

    def __init__(self, dimension: int):
        super().__init__(dimension)
        self._x_component: Expr = self._generate_random_field_component(dimension)
        self._y_component: Expr = self._generate_random_field_component(dimension)
        self._z_component: Expr = self._generate_random_field_component(dimension) if dimension == 3 else S.Zero
        C: CoordSys3D = CoordSys3D("C")
        self._field: Vector = self._x_component*C.i + self._y_component*C.j + self._z_component*C.k

