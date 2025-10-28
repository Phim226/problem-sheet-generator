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
        coeff_value_weights: list[float],
        index_weights: list[float]) -> list[int]:
    """
    Generate random weighted coefficients from a list of zeros.

    A list of zeros is created and then a weighted random subset is
    re-assigned to be non-zero. This is done to guarantee that some
    coefficients will be 0. That way, expressions built from them will
    tend to be simple but still exhibit sufficiently random behaviour.

    Parameters
    ==========
    max_index: int
        The maximum possible index that can be non-zero.

    non_zero_coeffs_range: tuple[int]
        A tuple (min, max) defining the minimum and maximum number of
        non-zero coefficients. Must satisfy 0 <= min <= max <= max_index.

    non_zero_coeff_weights: list[float]
        Weights for selecting the number of non-zero coefficients.
        For possible non-zero coefficients [1, 2, 3], with weights
        [0.7, 0.2, 0.1] then there will be one non-zero coefficient
        70% of the time, two 20% of the time and three 10% of the
        time. The weights are relative so don't need to sum to 1.

    coeff_value_range: tuple[int]
        A tuple (min, max) for the possible coefficient values. If
        0 is in the range then it will be removed.

    coeff_value_weights: list[float]
        Weights for the values of the non-zero coefficients.

    index_weights: list[float]
        Weights for the choice of index.

    Returns
    =======
    list[int]
        Random generated list of coefficients (many of which will
        be 0)

    Raises
    ======
    ValueError
        If non_zero_coeffs_range doesn't satisfy stated conditions.

        If max coefficient value is smaller than the minimum.

        If the lengths of the weights lists don't correspond to the
        number of possible values in their respective ranges. For the
        non-zero coefficients this is simply the difference in limits
        + 1. But for the coefficient values there may be 1 less value
        if 0 has been removed from the range.
    """
    non_zero_coeffs_min = non_zero_coeffs_range[0]
    non_zero_coeffs_max = non_zero_coeffs_range[1]
    if (non_zero_coeffs_min < 0 or  non_zero_coeffs_max > max_index):
        msg = ("Range of non-zero coefficients must be a subset of "
               "[0, max_index]")
        raise ValueError(msg)
    if non_zero_coeffs_max < non_zero_coeffs_min:
        msg = ("Maximum number of non-zero coefficients cannot smaller "
               "than the minimum.")
        raise ValueError(msg)

    non_zero_weights_len = len(non_zero_coeff_weights)
    non_zero_coeffs_len = non_zero_coeffs_max - non_zero_coeffs_min + 1
    if non_zero_weights_len != non_zero_coeffs_len:
        msg = ("The range of possible numbers of non-zero coefficients "
               "doesn't match the number of corresponding weights.")
        raise ValueError(msg)

    coeff_value_min = coeff_value_range[0]
    coeff_value_max = coeff_value_range[1]
    if coeff_value_max < coeff_value_min:
        msg = ("The maximum coefficient value cannot be smaller than "
               "the minimum value.")
        raise ValueError(msg)

    coeff_value_weights_len = len(coeff_value_weights)
    if coeff_value_min <= 0 <= coeff_value_max:
        coeff_value_len = coeff_value_max - coeff_value_min
    else:
        coeff_value_len = coeff_value_max - coeff_value_min + 1
    if coeff_value_weights_len != coeff_value_len:
        msg = ("The range of possible coefficient values "
               "doesn't match the number of corresponding weights.")
        raise ValueError(msg)

    if len(index_weights) != max_index:
        msg = ("The range of indices doesn't match the number of "
               "corresponding weights.")
        raise ValueError(msg)

    coeffs: list[int] = [0]*max_index

    number_of_coeffs: int = choices(
        population = range(
            non_zero_coeffs_min,
            non_zero_coeffs_max + 1
        ),
        weights = non_zero_coeff_weights
    )[0]

    coeff_range: list[int] = list(range(
        coeff_value_min,
        coeff_value_max + 1
        )
    )
    try:
        coeff_range.remove(0)
    except ValueError:
        pass

    index_range: list[int] = list(range(max_index))

    for _ in range(number_of_coeffs):
        index: int = choices(
            population = index_range,
            weights = index_weights
        )[0]
        index_range.remove(index)
        index_weights.pop(index)
        coeffs[index] = choices(
            population = coeff_range,
            weights = coeff_value_weights
        )[0]

    return coeffs