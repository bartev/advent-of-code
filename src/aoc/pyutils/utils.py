"""Common utlis to use in AOC files

Author: Bartev
Date: 2024-12-05

"""

import time


def time_it(func):
    """Use as a decorator on a function to time how long it takes to run

    E.g.

    @time_it
    def my_fun(args):
        pass
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to run")
        return result

    return wrapper


def flatten(lst: list[list]) -> list:
    """Flatten a list with mixed scalars and lists
    Recursive approach"""

    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))  # recursively flatten
        else:
            result.append(item)  # Add scalar item directly
    return result
