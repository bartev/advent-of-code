#!/usr/bin/env python

import logging
from pathlib import Path

from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import flatten, time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d11.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename):
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = [int(v) for v in f.read().split()]
    return content


class Puzzle:
    """Day 11 puzzle part 1"""

    def __init__(self, inputs: list[int]):
        "docstring"
        self.stones = inputs

    def rule_0_1(self, stone: int):
        """if stone = 0, convert to 1"""
        return 1 if stone == 0 else None

    def rule_even_digits(self, stone: int) -> list[int]:
        """if stone has even digits, return 2 stones"""
        str_stone = str(stone)

        stone_length = len(str_stone)
        if stone_length % 2 == 0:
            midpoint = stone_length // 2
            return [int(str_stone[:midpoint]), int(str_stone[midpoint:])]

    def rule_other_2024(self, stone: int):
        """default rule, multiply by 2024"""
        return 2024 * stone

    def apply_first_rule(self, stone: int):
        """Apply the first rule"""
        rules = [self.rule_0_1, self.rule_even_digits, self.rule_other_2024]
        for rule in rules:
            result = rule(stone)
            if result is not None:
                return result
        return None

    def blink(self):
        new_stones = [self.apply_first_rule(stone) for stone in self.stones]
        self.stones = flatten(new_stones)
        return self.stones


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str, blinks: int = 1) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    stones = read_data(filename)
    puzzle = Puzzle(stones)
    for i in range(blinks):
        cur_blink = puzzle.blink()
        # rprint(f"{i + 1}: {cur_blink}")
    return len(puzzle.stones)


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""test data: {part1('test_data_2.txt', blinks=6)}""")

rprint(f"""Problem input: {part1(fname, blinks=25)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
