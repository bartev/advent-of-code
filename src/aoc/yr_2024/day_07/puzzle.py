#!/usr/bin/env python

from pathlib import Path

from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

dname = Path("../../../../resources/2024/")
fname = dname / "d07.txt"
FNAME_TEST = "test_data.txt"

PRINT_STEP = False


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
    """True if x is evently divisible by y"""
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
    solvable_results = [t[0] for t, b in zip(contents, results) if b]
    return sum(solvable_results)


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


def concat_last_2(ys: list[int]) -> list[int]:
    """Concat the last 2 items"""
    if len(ys) > 1:
        p1, p2 = ys[:-2], ys[-2:]
        concat_2 = int("".join(map(str, p2)))
        p1.append(concat_2)
        res = p1
    else:
        res = []
    return res


def x_endsin(x: int, y: int) -> bool:
    """True if the number x ends in y"""
    return str(x).endswith(str(y))


def strip_y(x: int, y: int) -> int:
    """Remove y from the end of x (numbers)"""
    try:
        if x and y and x_endsin(x, y):
            return x == y or int(str(x).removesuffix(str(y)))
    except ValueException:
        breakpoint()


def solvable_2(x: int, ys: list[int], counter: int = 0) -> bool:
    """Similar recursion, but 3 cases now
    1. x/d, remaining_ys
    2. x - d, remaining_ys
    3. x, remaining_ys with last item concatenated with y
    """
    # if counter == 0:
    #     rprint(f"1st loop {x=}, {ys=}")

    # rprint(f"top of loop {x=}, {ys=}")
    # breakpoint()

    res = None
    if not ys:
        # Nothing left case
        res = None
    elif x is None or x < 0:
        res = None
    else:
        mysum = sum(ys)
        myconcat = int("".join(map(str, ys)))
        y = ys[-1]
        remaining_ys = ys[:-1]
        x_strip = strip_y(x, y)

        # rprint(f"{x=} --- {y=} ---  {ys=}")

        if not x:
            pass
        elif x == mysum:
            # Sum case
            res = True
            # rprint("in mysum check")
            # rprint(f"{x=} --- {y=} ---  {ys=}")
        elif x == myconcat:
            # Concatenate case
            res = True
            # rprint("in myconcat check")
            # rprint(f"{x=} --- {y=} ---  {ys=}")
        elif solvable_2(x - y, remaining_ys, counter + 1):
            # addition
            res = True
            # rprint("in add check")
            # rprint(f"{x=} --- {y=} ---  {ys=}")
        elif (
            y != 0 and divisible(x, y) and solvable_2(x // y, remaining_ys, counter + 1)
        ):
            res = True
            # rprint("in mult check")
            # rprint(f"{x=} --- {y=} ---  {ys=}")
        elif x_endsin(x, y) and solvable_2(x_strip, remaining_ys, counter + 1):
            # concatenation
            res = True

    if counter == 0 and PRINT_STEP:
        rprint(f"1st loop {res=}: {x=}, {ys=}")  #

    return res


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    contents = read_data(filename)
    results = [solvable_2(*item) for item in contents]
    solvable_results = [t[0] for t, b in zip(contents, results) if b]
    return sum(solvable_results)


rprint(f"""test data: {part2(FNAME_TEST)} (expected = 11387)""")
rprint(f"""Problem input: {part2(fname)} (expected = 264184041398847)""")
