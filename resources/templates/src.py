#!/usr/bin/env python

from pathlib import Path

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

console = Console()

dname = Path("../../../../resources/{{year}}/")
fname = dname / "d{{day}}.txt"
fname_test = "test_data.txt"

# ########## Part 1

rprint(Panel.fit("Part 1"))


def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    pass


console.print(f"""test data: {part1(fname_test)}""")

rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Panel.fit("Part 2"))


def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part2(fname_test)}""")

rprint(f"""Problem input: {part2(fname)}""")
