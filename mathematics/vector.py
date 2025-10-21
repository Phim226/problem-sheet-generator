import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from random import randint, choices
from utils import timing

@timing
def generate_random_vector_field(dimension: int = 3):
    number_of_coeffs: int = choices(population= range(1, 5), weights = [0.5, 0.3, 0.1, 0.05])[0]
    coeff_range: list = list(range(-4, 5))
    coeff_range.remove(0)
    coeffs = [(randint(0, 3*dimension), choices(population = coeff_range, weights =[0.05, 0.05, 0.1, 0.2, 0.3, 0.15, 0.1, 0.05])[0]) for _ in range(number_of_coeffs)]
    print(coeffs)

generate_random_vector_field()