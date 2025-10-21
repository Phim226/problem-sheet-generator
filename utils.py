from functools import wraps
from time import time
from typing import Callable

def timing(func: Callable) -> Callable:
    @wraps(func)
    def wrap(*args, **kwargs):
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        print(f"Function {func.__name__} took {time_end-time_start:2.5f} seconds to execute")
        return result
    return wrap