#!/usr/bin/env python

from pathlib import Path

from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

dname = Path("../../../../resources/2024/")
fname = dname / "d07.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""

    def read_line(line):
        x_part, y_part = line.strip().split(":")
        x = int(x_part.strip())
        ys = list(map(int, y_part.strip().split()))
        return x, ys

    with open(filename, "r") as f:
        content = [read_line(line) for line in f]
    return content


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


def divisible(x: int, y: int) -> bool:
    return x % y == 0


def solvable(x: int, ys: list[int]) -> bool:
    """True if applying + or * operators between each y can yield x
    Try recursing over smaller subsets.
    Apply from the end of ys
    """

    if not ys:
        return False

    # Check addition (avoid trying multiplication below)
    if x == sum(ys):
        # Stop here
        return True

    # Iterate over possible splits in the list

    y = ys[-1]
    remaining_ys = ys[:-1]

    # Check addition
    if solvable(x - y, remaining_ys):
        return True

    if y != 0 and divisible(x, y):
        return solvable(x // y, remaining_ys)


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    contents = read_data(filename)
    results = [solvable(*item) for item in contents]
    solveable_results = [t[0] for t, b in zip(contents, results) if b]
    return sum(solveable_results)


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
