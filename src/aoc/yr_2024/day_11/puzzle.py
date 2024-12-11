#!/usr/bin/env python

import cProfile
import logging
import pstats
from functools import lru_cache
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
        return [1] if stone == 0 else None

    def rule_even_digits(self, stone: int) -> list[int]:
        """if stone has even digits, return 2 stones"""
        str_stone = str(stone)

        stone_length = len(str_stone)
        if stone_length % 2 == 0:
            midpoint = stone_length // 2
            return [int(str_stone[:midpoint]), int(str_stone[midpoint:])]

    def rule_other_2024(self, stone: int):
        """default rule, multiply by 2024"""
        return [2024 * stone]

    @lru_cache(maxsize=None)  # Cache unlimited results
    def apply_first_rule(self, stone: int) -> list:
        """Apply the first rule"""
        rules = [self.rule_0_1, self.rule_even_digits, self.rule_other_2024]
        for rule in rules:
            result = rule(stone)
            if result is not None:
                return result
        return None

    def blink_5_single(self, stone):
        # print(f"{stone=}")
        stones_1 = [self.apply_first_rule(st) for st in [stone]]
        # print(f"{stones_1=}")
        stones_2 = [self.apply_first_rule(st) for st in flatten(stones_1)]
        stones_3 = [self.apply_first_rule(st) for st in flatten(stones_2)]
        stones_4 = [self.apply_first_rule(st) for st in flatten(stones_3)]
        stones_5 = [self.apply_first_rule(st) for st in flatten(stones_4)]
        return flatten(stones_5)

    def blink_5(self):
        new_stones = [self.blink_5_single(stone) for stone in self.stones]
        self.stones = flatten(new_stones)
        return self.stones

    def blink(self):
        new_stones = [self.apply_first_rule(stone) for stone in self.stones]
        self.stones = flatten(new_stones)
        return self.stones

    def blinkr(self, stones: list[int], blinks: int = 0) -> int:
        """Count how many stones are there after blinking `blinks` times
        Uses a recursive algorithm
        """

        def helper(xs: list[int], acc: int = 0) -> int:
            """Recursive function with accumulator to track blinks left"""
            # rprint(f"{acc=}, {xs=}")
            # breakpoint()
            if not xs:
                res = 0
            if acc >= blinks:
                res = len(xs)
            else:  #  acc < blinks
                to_operate_on = [self.apply_first_rule(stone=y) for y in xs]
                # rprint(f"{to_operate_on=}")
                # breakpoint()
                res = sum([helper(y, acc + 1) for y in to_operate_on])

            return res

        answer = helper([stones], acc=0)

        return answer


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str, blinks: int = 1) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    stones = read_data(filename)
    puzzle = Puzzle(stones)
    for _ in range(blinks):
        puzzle.blink()
    return len(puzzle.stones)


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""test data: {part1('test_data_2.txt', blinks=6)}""")

rprint(f"""Problem input: {part1(fname, blinks=25)}""")
rprint(f"""Problem input: {part1(fname, blinks=35)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


# def explore():
#     """EDA"""
#     for i in range(1):
#         stones = [i]
#         puzzle = Puzzle(stones)
#         rprint(Panel.fit(f"[bold red]Stones = {stones}"))
#         rprint(f"0: {stones}")
#         blink_counter = 1
#         cur_blink = puzzle.blink()
#         rprint(f"{blink_counter}: {cur_blink}")
#         while i not in cur_blink:
#             blink_counter += 1
#             cur_blink = puzzle.blink()
#             rprint(f"{blink_counter}: {cur_blink}")
#         rprint(
#             Panel.fit(
#                 f"[yellow] Starting stones = {stones}. {blink_counter} blinks to see starting stone"
#             )
#         )


# @time_it
# def explore2(blinks: int = 1):
#     """EDA"""
#     for start_stone in range(10):
#         stones = [start_stone]
#         puzzle = Puzzle(stones)
#         rprint(Panel.fit(f"[bold red]Stones = {stones}"))
#         rprint(f"0: {stones}")
#         for blink_counter in range(blinks):
#             cur_blink = puzzle.blink()
#             rprint(f"{blink_counter}: {cur_blink}")


# @time_it
# def explore3(blinks: int = 5):
#     """EDA"""
#     for start_stone in range(10):
#         stones = [start_stone]
#         puzzle = Puzzle(stones)
#         rprint(Panel.fit(f"[bold red]Stones = {stones}"))
#         rprint(f"0: {stones}")
#         cur_blink = puzzle.blink_5_single(start_stone)
#         rprint(f"{cur_blink=}")


@time_it
def part2(filename: str = None, stones: list[int] = None, blinks: int = 1) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    # stones = [0]
    stones = read_data(filename) if filename else stones
    # rprint(f"{blinks=}, {stones=}")
    puzzle = Puzzle(stones)
    # rprint(f"0: {stones}")
    # for i in range(8):
    #     print(f"blink count: {i}")
    #     puzzle.blink_5()
    #     # cur_blink = puzzle.blink()
    #     # rprint(f"{i + 1}: {cur_blink}")
    # return len(puzzle.stones)
    answers = [puzzle.blinkr(stone, blinks=blinks) for stone in stones]
    return sum(answers)


# for blink in range(2):
#     rprint(f"""part 2 : {part2('test_data_empty.txt', blinks=blink)}""")

# for blinks in range(4):
#     rprint(Panel.fit(f"""part 2: {part2(stones=[], blinks = blinks)}"""))
#     rprint(Panel.fit(f"""part 2: {part2(stones=[0], blinks = blinks)}"""))

# for blinks in range(7):
#     rprint(Panel.fit(f"""part 2: {part2(stones=[0], blinks = blinks)}"""))

rprint(f"""test input: {part2(filename=FNAME_TEST, blinks=1)}""")
rprint(f"""test input: {part2(filename="test_data_2.txt", blinks=6)}""")
rprint(f"""Problem input: {part2(fname, blinks=25)}""")
rprint(f"""Problem input: {part2(fname, blinks=35)}""")

# explore()
# explore2(blinks=5)

# explore3(blinks=5)

# cProfile.run("part2(fname, blinks=75)", "profile_output")
# Display the results
# with open("profile_results.txt", "w") as f:
#     stats = pstats.Stats("profile_output", stream=f)
#     stats.strip_dirs()
#     stats.sort_stats("cumulative")
#     stats.print_stats()
