#!/usr/bin/env python

import cProfile
import logging
import pstats
from collections import Counter, defaultdict
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

    def blink(self):
        new_stones = [self.apply_first_rule(stone) for stone in self.stones]
        self.stones = flatten(new_stones)
        return self.stones

    def blink_n(self, stones: list[int], blinks: int = 0):
        """Solve this with O(blinks). Use a Counter with stone values
        as the keys, and the number of times they appear as the values.
        """

        def helper(stone_ctr: dict, acc: int = 0) -> Counter:
            """xs is a dict with stones as keys, and count of stones as values"""
            # breakpoint()

            if not stone_ctr:
                # should never happen except for degenerate case of empty dict
                res = Counter()
            elif acc >= blinks:  # stopping condition
                res = stone_ctr
            else:  # recurse acc < blinks
                # We have 2 dictionaries
                # INPUT:             stone_ctr:      {stone : num_instances}
                # INTERMEDIATE_STEP: stones_xformed: {stone : blink(stone)}
                # RESULT:            output:         {blink(stone) : num_instances}

                output = defaultdict(int)
                # Apply blink to every key in stone_ctr, keeping track of the
                # stone, and its transformation
                stones_xformed = {
                    stone: self.apply_first_rule(stone) for stone in stone_ctr
                }

                for stone, xforms in stones_xformed.items():
                    for new_stone in xforms:  # xforms are lists of len 1 or 2
                        # How many times was this stone in the original list?
                        # Keep track so we can count correctly going forward
                        to_add = stone_ctr.get(stone, 1)
                        # If a stone showed up multiple times in stones_xformed,
                        # we add stone_ctr[stone] to the output that many times
                        # via the loop. No need to multiply
                        output[new_stone] += to_add
                res = helper(output, acc + 1)
            return Counter(res)

        # Start with a Counter {stone: num_instances}
        stone_counter = Counter(stones)
        final_counter = helper(stone_counter, acc=0)

        return final_counter.total()


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


# rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname, blinks=25)}""")


# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str = None, stones: list[int] = None, blinks: int = 1) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    stones = read_data(filename) if filename else stones
    puzzle = Puzzle(stones)
    return puzzle.blink_n(stones, blinks=blinks)


rprint(f"""25 blinks: {part2(fname, blinks=25)}""")
rprint(f"""75 blinks: {part2(fname, blinks=75)}""")


def profile_1():
    rprint("Run part 1 25 blinks")
    cProfile.run("part1(fname, blinks=25)", "profile_output_1")
    # Display the results
    with open("profile_results_1.txt", "w", encoding="utf8") as f:
        stats = pstats.Stats("profile_output_1", stream=f)
        stats.strip_dirs()
        stats.sort_stats("cumulative")
        stats.print_stats()


def profile_2():
    rprint("Run part 2 25 blinks")
    cProfile.run("part2(fname, blinks=25)", "profile_output_2")
    # Display the results
    with open("profile_results_2.txt", "w", encoding="utf8") as f:
        stats = pstats.Stats("profile_output_2", stream=f)
        stats.strip_dirs()
        stats.sort_stats("cumulative")
        stats.print_stats()


profile_1()
profile_2()
