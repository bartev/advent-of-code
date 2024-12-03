#!/usr/bin/env python

from pathlib import Path

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

console = Console()

DATA = """
"""

dname = Path("../../../../resources/{{year}}/")
fname = dname / "d{{day}}.txt"

rprint(Panel.fit("Part 1"))


def part1(data_str: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    pass


console.print(f"""test data: {part1(DATA)}""")


with open(fname, "r") as f:
    input_data = f.read()

rprint(f"""Problem input: {part1(input_data)}""")


rprint(Panel.fit("Part 2"))


def part2(data_str: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part2(DATA)}""")

rprint(f"""Problem input: {part2(input_data)}""")
