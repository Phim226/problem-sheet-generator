from functools import wraps
from time import time
from typing import Callable
import logging

def timing(func: Callable) -> Callable:
    @wraps(func)
    def wrap(*args, **kwargs):
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        print(f"Function {func.__name__} took {time_end-time_start:2.5f} seconds to execute")
        return result
    return wrap

def configure_log() -> None:
    level = logging.DEBUG
    format = "[%(levelname)s] - %(message)s"
    logging.basicConfig(level = level, format = format)