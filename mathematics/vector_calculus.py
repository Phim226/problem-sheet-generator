from random import choices
from sympy.vector import CoordSys3D

class ScalarField():
    def __init__(self):
        pass

class VectorField():

    def __init__(self, dimension: int, C: CoordSys3D, randomly_generated: bool = True):
        pass

""" The method of random generation is we generate weighted random coefficients for the polynomial
    (c_0x^2 + c_1x + c_2)(c_3y^2 + c_4y + c_5)(c_6z^2 + c_7z + c_8) and then evaluate the product.
    This way we get a polynomial in x, y and z of max total degree 6 consisting of 26 possible
    combinations of the multivariate monomial (x^n)(y^m)(z^t) with 0<=n,m,t<=2 plus a possible 
    constant term, with only a small handful of coefficients being generated. If the dimension is
    2 then we don't generate values for c_6, c_7 and c_8.
    
    To avoid each component being overly populated with monomials we first set all coefficients to be
    0 and then randomly choose at most 4 to be non-zero. The random generation of the number of non-zero 
    coefficients variable number_of_coeffs is weighted. For the weighting [0.6, 0.3, 0.07, 0.03] this 
    produces 1 non-zero coefficient 60% of the time, 2 non-zero coefficients 30% of the time and so on. 
    So with this weighting we aim to have simple expressions be most common.

    The value of the coefficients is also weighted. A weighting [0.01, 0.05, 0.05, 0.1, 0.4, 0.2, 0.1, 0.09]
    for the range of possible values [-4, -3, -2, -1, 1, 2, 3, 4] produces coefficients that tend towards
    lower absolute values with a bias towards positive numbers (-1 is 10%, 1 is 40%, -2 is 5%, 2 is 20% and so on).

    Note that if the number of coefficients or the range of possible coefficient values is changed then the
    weightings should be changed accordingly as well, otherwise you might get a ValueError if the number of
    weights doesn't match.     
    """
def generate_random_vector_field_component(dimension: int, C: CoordSys3D):
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
    x_coeffs = coeffs[0:3]
    y_coeffs = coeffs[3:6]
    z_coeffs = coeffs[6:9] if dimension == 3 else None
    component_x_terms = 1 if all(c==0 for c in x_coeffs) else x_coeffs[0]*C.x**2 + x_coeffs[1]*C.x + x_coeffs[2]
    component_y_terms = 1 if all(c==0 for c in y_coeffs) else y_coeffs[0]*C.y**2 + y_coeffs[1]*C.y + y_coeffs[2]
    component_z_terms = 1 if not z_coeffs or all(c==0 for c in z_coeffs) else z_coeffs[0]*C.z**2 + z_coeffs[1]*C.z + z_coeffs[2]
    return component_x_terms*component_y_terms*component_z_terms

def generate_random_vector_field(dimension: int, C: CoordSys3D):
    x_component = generate_random_vector_field_component(dimension, C)
    y_component = generate_random_vector_field_component(dimension, C)
    z_component = generate_random_vector_field_component(dimension, C) if dimension == 3 else 0
    F = x_component*C.i + y_component*C.j + z_component*C.k
    return F
