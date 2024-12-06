#!/usr/bin/env python

from pathlib import Path

from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

dname = Path("../../../../resources/{{year}}/")
fname = dname / "d{{day}}.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = f.read()
    return content

# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))

@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit([bold red]"Part 2"))

@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
