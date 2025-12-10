from random import choices, randint
from more_itertools import distinct_permutations
from sympy import Expr, Rational, Symbol
from sympy.combinatorics import IntegerPartition

# TODO: Write docstrings, especially for polynomial_from_coeffs (coeff index corresponds inversely to degree)
def polynomial_from_coeffs(p: Symbol, coeffs: list[int]) -> Expr:
    poly: Expr = 0
    degree: int = len(coeffs) - 1
    for index, coeff in enumerate(coeffs):
        poly += coeff*p**(degree - index)
    return poly

def weak_compositions(n: int, k: int) -> list[list[int]]:
    """
    Returns all weak compositions of the positive integer n into k parts.

    In other words this function returns all the solutions of the equation

        x_1 + x_2 + ... + x_k = n

    where each x_i is a non-negative integer.

    Parameters
    ==========
    n: int
        The integer we want to find the compositions of.

    k: int
        The number of parts we are splitting n into. If k<=0 then the function returns an empty
        list.

    Examples
    ========
    >>> all_non_neg_integer_comps(3, 2):
    [[3, 0], [2, 1], [1, 2], [0, 3]]
    """
    if n == 0:
        return []

    n: list[int] = [n]
    partitions: list[list[int]] = [n]
    partition = IntegerPartition(n)
    prev = partition.prev_lex()

    while prev.partition != n:
        partitions.append(prev.partition)
        partition = IntegerPartition(prev.partition)
        prev = partition.prev_lex()

    unordered_comps = []
    for part in partitions:
        if len(part) > k:
            continue

        part += [0]*(k - len(part))
        unordered_comps.append(part)

    ordered_comps = sum((list(distinct_permutations(comp)) for comp in unordered_comps), [])

    return ordered_comps

def random_weighted_coefficients(
        max_index: int,
        non_zero_coeffs_range: tuple[int],
        coeff_value_range: tuple[int],
        non_zero_coeff_weights: list[float] = None,
        coeff_value_weights: list[float] = None,
        index_weights: list[float] = None
    ) -> list[int]:
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

    coeff_value_range: tuple[int]
        A tuple (min, max) for the possible coefficient values. If
        0 is in the range then it will be removed.

    non_zero_coeff_weights: list[float], optional
        Weights for selecting the number of non-zero coefficients.
        For possible non-zero coefficients [1, 2, 3], with weights
        [0.7, 0.2, 0.1] then there will be one non-zero coefficient
        70% of the time, two 20% of the time and three 10% of the
        time. The weights are relative so don't need to sum to 1.
        Default value is None.

    coeff_value_weights: list[float], optional
        Weights for the values of the non-zero coefficients. Default
        value is None.

    index_weights: list[float], optional
        Weights for the choice of index. Default value is None.

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
        plus 1. But for the coefficient values there may be 1 less value
        if 0 has been removed from the range.
    """
    non_zero_coeffs_min = non_zero_coeffs_range[0]
    non_zero_coeffs_max = non_zero_coeffs_range[1]
    if (non_zero_coeffs_min < 0 or  non_zero_coeffs_max > max_index):
        msg = ("Range of non-zero coefficients must be a subset of "
               "[0, max_index]")
        raise ValueError(msg)
    if non_zero_coeffs_max < non_zero_coeffs_min:
        msg = ("Maximum number of non-zero coefficients cannot be "
               "smaller than the minimum.")
        raise ValueError(msg)

    coeff_value_min = coeff_value_range[0]
    coeff_value_max = coeff_value_range[1]
    if coeff_value_max < coeff_value_min:
        msg = ("The maximum coefficient value cannot be smaller than "
               "the minimum.")
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
        index_weights.pop(index_range.index(index))
        index_range.remove(index)
        coeffs[index] = choices(
            population = coeff_range,
            weights = coeff_value_weights
        )[0]

    return coeffs

# TODO: Add weighting to small limit range
# TODO: Make generation of larger limit range correspond to weight increase toward simpler expressions (or vice versa)
def random_limits(
        min_limit: int,
        max_limit: int
) -> tuple[int, int]:
    lower_limit = randint(min_limit, max_limit - 1)
    return lower_limit, randint(lower_limit + 1, max_limit)

def awkward_number(num: Expr) -> bool:
    if isinstance(num, Rational):
        return _awkward_rational(num)
    return False

def _awkward_rational(rat: Rational) -> bool:
    num_str = str(rat.p)
    den_str = str(rat.q)
    num_str.replace("-", "")
    if len(num_str) > 3:
        return True
    if len(den_str) > 3:
        return True
    return False

