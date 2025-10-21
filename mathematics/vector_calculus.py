from random import choices
from sympy.vector import CoordSys3D


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
    z_coeffs = None if dimension == 2 else coeffs[6:9]
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
