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
    """
    Helper function to generate random weighted coefficients from a list
    of zeros.

    A list of zeros is defined. Then a weighted random selection of them
    will be re-assigned to be non-zero. This is done to guarantee that
    some coefficients will be 0. That way, expressions built from them
    will tend to be simple but still exhibit sufficiently random behaviour.

    Parameters
    =========

    max_index: int

        The maximum possible index that can be non-zero. In practice
        this determines the length of the initial list of zeros.

    non_zero_coeffs_range: tuple[int]

        A tuple defining the minimum and maximum number of coefficients
        in the list of zeros that will be set to be non-zero. So for
        a tuple (a, b) we must have a <= b, a >= 0 and b <= max_index.
        Then the number of non-zero coefficients will be randomly
        chosen, according to the relevant weights, from the list
        [a, a + 1, a + 2, ..., b - 1, b].

    non_zero_coeff_weights: list[float]

        The list containing the weights for selecting the number of
        non-zero coefficients. So the length of this list must be
        equal to the length of [a, a + 1, a + 2, ..., b - 1, b] or
        a ValueError will be thrown. For a list of possible non-zero
        coefficients [1, 2, 3], if the weights are [0.7, 0.2, 0.1]
        then 70% of the time only one coefficient will be non-zero,
        20% of the time two coefficients will be non-zero and 10%
        of the time 3 coefficients will be non-zero. The weights
        are relative so don't need to sum to 1. If the weights
        don't sum to 1 then you can calculate the actual probability
        of each choice by

                p = weight/sum of weights

        So if the sum of weights = 1 then p = weight.

    coeff_value_range: tuple[int]

        A tuple defining the minimum and maximum possible value
        of the non-zero coefficients. So for (a, b) we must have
        a <= b. If 0 is in (a, b) then it will be removed. Then
        the value of the coefficient is randomly chosen, according
        to the relevant weights, from the list
        [a, a + 1, a + 2, ..., b - 1, b].

    coeff_value_weights: list[float]

        The list of weights for the values of the non-zero
        coefficients. The length of this list must be equal to the
        length of the list of possible coefficient values. Care
        should be taken here since the list of possible values may
        be shorter than expected since 0 might have been removed if
        a < 0 and b > 0. See above in the description of
        non_zero_coeff_weights for more information on the impact
        of the weights on probability.
    """
    coeffs: list[int] = [0]*max_index

    number_of_coeffs: int = choices(
        population = range(
            non_zero_coeffs_range[0],
            non_zero_coeffs_range[1] + 1
        ),
        weights = non_zero_coeff_weights
    )[0]

    coeff_range: list[int] = list(range(
        coeff_value_range[0],
        coeff_value_range[1] + 1
        )
    )
    try:
        coeff_range.remove(0)
    except ValueError:
        pass

    index_range: list[int] = list(range(max_index))

    for _ in range(number_of_coeffs):
        index: int = choice(index_range)
        index_range.remove(index)
        coeffs[index] = choices(
            population = coeff_range,
            weights = coeff_value_weights
        )[0]

    return coeffs