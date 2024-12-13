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


def series_from(num: int, incr: int = 1) -> int:
    """Create an generator for integers starting from `num`
    Ex:
    # Create the series 3, 5, 7, ...
    s = series_from(3, incr=2)
    next(s) # 3
    next(s) # 5
    """
    while True:
        yield num
        num += incr


def find_continuous_values(lst: list[int], increasing: bool = True) -> list[list[int]]:
    """Find all continuous values in xs

    lst: list of integers
    increasing: true if going up, false if going down

    Example:

      xs = [1, 2, 3, 5, 9, 10, 11]
      find_continuous_values(xs)
      > [[1, 2, 3], [5], [9, 10, 11]]
    """
    result = []
    if not lst:
        return result  # Return an empty list if the input is empty

    xs = sorted(lst, reverse=not increasing)
    incr = 1 if increasing else -1

    current_group = [xs[0]]
    for i in range(1, len(xs)):
        if xs[i] == xs[i - 1] + incr:  # incr is either +/- 1
            current_group.append(xs[i])
        else:
            result.append(current_group)
            current_group = [xs[i]]
    result.append(current_group)  # Append the last group
    return result


def find_continuous_values_ge(n: int, lst: list[int]) -> list[int]:
    """Find all continuous values from n that are >= n in list
    If n is not in the list, return an empty list.

    Example
    ys = [1, 2, 3, 5, 9, 10, 11]
    print(find_continuous_values_ge(2, ys))
    print(find_continuous_values_ge(4, ys))
    print(find_continuous_values_ge(5, ys))

    """
    xs = [item for item in lst if item >= n]
    # We only want the first list of items
    res = find_continuous_values(xs, increasing=True)[0] if n in xs else []
    return res


def find_continuous_values_le(n: int, lst: list[int]) -> list[int]:
    """Find all continuous values from n that are <= n in list
    If n is not in the list, return an empty list.

    Example
    ys = [1, 2, 3, 5, 9, 10, 11]
    print(find_continuous_values_le(2, ys))
    print(find_continuous_values_le(4, ys))
    print(find_continuous_valuesz_le(5, ys))
    """
    xs = [item for item in lst if item <= n]
    # We only want the first list of items
    res = find_continuous_values(xs, increasing=False)[0] if n in xs else []
    return res
