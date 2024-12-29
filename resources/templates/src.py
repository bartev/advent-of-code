#!/usr/bin/env python

import functools
import heapq
import logging
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

import pyperclip as pc
import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

# from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

script_dir = Path(__file__).parent

dname = Path("../../../../resources/{{year}}/")
fname = dname / "d{{day}}.txt"
FNAME_TEST = "test_data.txt"

sys.setrecursionlimit(10**6)
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up right down left


def ints(s):
    """Return a list of all ints in s
    Example:
    > ints('xy2b-34y5-6z')
    [2, -34, 5, -6]
    """
    return [int(x) for x in re.findall(r"-?\d+", s)]


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        content = f.read()
    return content


# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""


rich.print(f"""test data: {part1(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rich.print(f"""test data: {part2(FNAME_TEST)}""")
rich.print(f"""Problem input: {part2(fname)}""")
