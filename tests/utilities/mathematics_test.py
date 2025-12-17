from random import randint
from sympy import Rational, S, pi, sqrt
from utilities import weak_compositions, awkward_number

def test_weak_compositions(subtests):
    random_int = randint(1, 100)
    random_neg_int = randint(-100, -1)
    weak_comps_test_cases = {
        (0, 0): [],
        (random_int, 0): [],
        (random_int, 1): [(random_int,)],
        (random_int, random_neg_int): [],
        (1, 2): [(0, 1), (1, 0)],
        (2, 2): [(0, 2), (2, 0), (1, 1)],
        (3, 2): [(0, 3), (3, 0), (1, 2), (2, 1)]
    }

    for i, (input, output) in enumerate(weak_comps_test_cases.items()):
        with subtests.test("Weak composition test cases", i = i):
            assert weak_compositions(*input) == output

def test_awkward_number(subtests):
    awkward_test_cases = {
        0: False,
        1: False,
        S.One: False,
        S.Zero: False,
        pi: False,
        Rational(1, 2): False,
        Rational(15, 7): False,
        1000: True,
        -1000: True,
        999: False,
        Rational(999, 998): False,
        Rational(1000, 999): True,
        Rational(2340920492034, 34920): True,
        Rational(-209323984093422340920492034, 2903482903428937492387434920): True,
        sqrt(2): False,
        sqrt(1000): False
    }

    for i, (input, output) in enumerate(awkward_test_cases.items()):
        with subtests.test("Weak composition test cases", i = i):
            assert awkward_number(input) == output