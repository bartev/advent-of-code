#!/usr/bin/env python

import logging
from pathlib import Path

import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d19.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        towels = [towel.strip() for towel in f.readline().strip().split(",")]
        patterns = [line.strip() for line in f if line.strip()]
    return towels, patterns


# read_data(FNAME_TEST)

# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


def find_towel_combos(towels, design):
    """Find all towel combinations that can create design"""

    def helper(current_design, path):
        """The recursive function helper"""
        # base case: if current_design is empty, we have found a path
        if not current_design:
            return [path]

        valid_towels = [towel for towel in towels if current_design.startswith(towel)]

        # Recursively check each towel
        combinations = []
        for towel in valid_towels:
            remaining_design = current_design.removeprefix(towel)
            combinations.extend(helper(remaining_design, path + [towel]))
        return combinations

    # Start the call with the whole design and an empty list
    return helper(design, [])


def can_be_formed(design, towels):
    """True if design can be formed with towels"""
    # breakpoint()

    if not design:
        return True

    for towel in towels:
        remainder = design.removeprefix(towel)
        if remainder != design:  # means towel was successfully returned
            if can_be_formed(remainder, towels):
                return True
    return False


def reduce_redundancies_towels(towels):
    """Reduce the number of keys in towels.
    e.g., if I have b, bb, and bbb, I can replace all of these by b."""
    # Sort towels by length to get smallest units
    sorted_towels = sorted(towels, key=lambda x: (len(x), x))
    # store strings that cannot be formed by combinations of other strings
    reduced_towels = []
    redundant_towels = []
    # breakpoint()
    for towel in sorted_towels:
        # Check if towel can be formed from shorter towels
        if not can_be_formed(towel, reduced_towels):
            reduced_towels.append(towel)
        else:
            redundant_towels.append(towel)
    return reduced_towels, redundant_towels


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    towels, designs = read_data(filename)
    # Reduce complexity by removing towels that can be formed from smaller ones
    reduced_towels, _ = reduce_redundancies_towels(towels)
    rich.print(f"{len(towels)=}, {len(reduced_towels)=}")
    # can_form_design is a list of bools, true if it can be formed
    can_form_design = [can_be_formed(design, reduced_towels) for design in designs]
    return sum(can_form_design)


rich.print(f"""test data: {part1(FNAME_TEST)}""")
print()
rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    towels, designs = read_data(filename)
    # Reduce complexity by removing towels that can be formed from smaller ones
    reduced_towels, redundant_towels = reduce_redundancies_towels(towels)

    valid_designs = [
        design for design in designs if can_be_formed(design, reduced_towels)
    ]
    return len(valid_designs)


# rich.print(f"""test data: {part2(FNAME_TEST)}""")
rich.print(f"""Problem input: {part2(fname)}""")
