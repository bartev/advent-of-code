#!/usr/bin/env python


from pathlib import Path

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

console = Console()

DATA = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

dname = Path("../../../../resources/2024/")
fname = dname / "d02.txt"
fname_test = "test_data.txt"

# ########## Part 1

rprint(Panel.fit("Part 1"))


def read_as_rows(filename: str) -> list[int]:
    """Read a list of row data, each row containing several ints
    separated by spaces.  Return a list of list of ints
    """
    with open(filename, "r") as f:
        result = [[int(num) for num in line.strip().split()] for line in f]
    return result


def calc_diffs(row: list[int]) -> list[int]:
    return [row[i] - row[i - 1] for i in range(1, len(row))]


def get_diffs_from_fname(filename: str) -> list[list[int]]:
    data = read_as_rows(filename)
    return [calc_diffs(row) for row in data]


# Filter rows
def crit_1(row: list[int]) -> bool:
    return all(x > 0 for x in row) or all(x < 0 for x in row)


def crit_2(row: list[int]) -> bool:
    return all(abs(x) >= 1 for x in row) and all(abs(x) <= 3 for x in row)


def check_criteria(row: list[int]) -> bool:
    return crit_1(row) and crit_2(row)


def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution
    Return how many reports are safe
    """
    diffs = get_diffs_from_fname(filename)
    filtered_rows = [row for row in diffs if check_criteria(row)]
    return len(filtered_rows)


console.print(f"""test data: {part1(fname_test)}""")

rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Panel.fit("Part 2"))


def keep_row_with_damp(row: list[int]) -> bool:
    """True if the row passes all criteria,
    if drop any single item (or none)

    The row here is raw data, and must be converted to diffs
    """
    # Check the entire list
    if check_criteria(calc_diffs(row)):
        return row

    # Check subsets
    for i in range(len(row)):
        subset = row[:i] + row[i + 1 :]
        if check_criteria(calc_diffs(subset)):
            return row

    # Default is false
    return None


def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    # This time, read all data into a list of list[int]
    data = read_as_rows(filename)
    valid_with_damp = [keep_row_with_damp(row) for row in data]

    return len([row for row in valid_with_damp if row])


rprint(f"""test data: {part2(fname_test)}""")

rprint(f"""Problem input: {part2(fname)}""")
