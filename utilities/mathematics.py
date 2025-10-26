from random import choice, choices
from sympy import Expr, Symbol

def build_polynomial_from_coeffs(p: Symbol, coeffs: list[int]) -> Expr:
    poly: Expr = 0
    degree: int = len(coeffs) - 1
    for index, coeff in enumerate(coeffs):
        poly += coeff*p**(degree - index)
    return poly

def generate_non_zero_weighted_coefficients(
        max_index: int,
        non_zero_coeffs_range: tuple[int],
        non_zero_coeff_weights: list[float],
        coeff_value_range: tuple[int],
        coeff_value_weights: list[float]) -> list[int]:

    possible_num_non_zero_coeffs = (non_zero_coeffs_range[1]
                                    - non_zero_coeffs_range[0] + 1)
    if len(non_zero_coeff_weights) != possible_num_non_zero_coeffs:
        raise ValueError(("The number of weights doesn't match the choice "
                          "of numbers of non-zero coefficients. There are "
                          f"{len(non_zero_coeff_weights)} weights and "
                          f"{possible_num_non_zero_coeffs} possible values "
                          "for the number of non-zero coefficients."))

    num_coeff_values = (coeff_value_range[1] -
                        coeff_value_range[0])
    if len(coeff_value_weights) != num_coeff_values:
        raise ValueError(("The number of possible coefficient values "
                          "doesn't match the number of weights. There are "
                          f"{len(coeff_value_weights)} weights and "
                          f"{num_coeff_values} possible values "
                          "for the coefficients."))

    coeffs: list[int] = [0]*max_index

    min_num_non_zero = non_zero_coeffs_range[0]
    max_num_non_zero = non_zero_coeffs_range[1]
    number_of_coeffs: int = choices(
        population = range(min_num_non_zero, max_num_non_zero + 1),
        weights = non_zero_coeff_weights
    )[0]

    smallest_coeff_value = coeff_value_range[0]
    highest_coeff_value = coeff_value_range[1]
    coeff_range: list[int] = list(range(
        smallest_coeff_value,
        highest_coeff_value + 1
        )
    )
    coeff_range.remove(0)

    index_range: list[int] = list(range(max_index))

    for _ in range(number_of_coeffs):
        index: int = choice(index_range)
        index_range.remove(index)
        coeffs[index] = choices(
            population = coeff_range,
            weights = coeff_value_weights
        )[0]

    return coeffs