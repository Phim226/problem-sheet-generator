from functools import wraps
from inspect import getfullargspec
from logging import basicConfig, DEBUG
from time import time
from typing import Callable



BLUE = "\033[34m"
RESET = "\033[0m"

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
    level = DEBUG
    format = "[%(levelname)s] - %(message)s"
    basicConfig(level = level, format = format)

def get_kwargs(func: Callable):
    spec = getfullargspec(func)
    kwargs = {key: value for key, value in zip(
        reversed(spec.args),
        reversed(spec.defaults)
        )
    }
    return dict(list(reversed(kwargs.items())))