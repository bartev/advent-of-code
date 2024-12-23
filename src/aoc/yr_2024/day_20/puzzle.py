#!/usr/bin/env python

import logging
from collections import Counter
from pathlib import Path

import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.grid_points import Grid, Point
from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d20.txt"
FNAME_TEST = "test_data.txt"


class PGrid(Grid):
    """Assumes there is 1 path through the maze"""

    def __init__(self, filename: str):
        """Grid for this puzzle"""
        super().__init__(filename=filename)
        logger.debug(f"{self.rows=}, {self.cols=}")
        self.start = self.find_char("S")
        self.end = self.find_char("E")
        self.track = self.number_maze_steps()
        self.cheats = {}  # (one_over, two_over): steps saved

    direc_incrs = {"n": (-1, 0), "s": (1, 0), "e": (0, 1), "w": (0, -1)}
    directions = direc_incrs.keys()
    valid_points = ".ES"

    def find_char(self, char: str = "S"):
        """Find the Point that contains `char`"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.get((row, col)) == char:
                    return (row, col)

    def number_maze_steps(self):
        """Start at `start`, end at `end`, and number steps to get there"""
        cur_point = self.start
        counter = 0
        steps = {}
        while self.get(cur_point) in self.valid_points:
            steps[cur_point] = counter
            if (
                self.in_grid(next_point := self.point_above(cur_point))
                and self.get(next_point) in self.valid_points
                and next_point not in steps
            ):
                counter += 1
                cur_point = next_point
            elif (
                self.in_grid(next_point := self.point_right(cur_point))
                and self.get(next_point) in self.valid_points
                and next_point not in steps
            ):
                counter += 1
                cur_point = next_point
            elif (
                self.in_grid(next_point := self.point_below(cur_point))
                and self.get(next_point) in self.valid_points
                and next_point not in steps
            ):
                counter += 1
                cur_point = next_point
            elif (
                self.in_grid(next_point := self.point_left(cur_point))
                and self.get(next_point) in self.valid_points
                and next_point not in steps
            ):
                counter += 1
                cur_point = next_point
            else:
                break
        return steps

    def check_2(self, start: Point, dp: Point):
        """Check 2 steps over
        if start + dp is a wall
        and start + 2xdp is a valid point
        and steps(start + 2xdp) > steps(start)
        then add to cheats"""
        x, y = start
        dx, dy = dp
        one_over = (x + dx, y + dy)
        two_over = (x + 2 * dx, y + 2 * dy)

        if (
            self.in_grid(two_over)
            and self.get(one_over) == "#"
            and self.get(two_over) in self.valid_points
            and self.track[two_over] > self.track[start]
        ):
            self.cheats[(one_over, two_over)] = (
                self.track[two_over] - self.track[start] - 2
            )

    def check_point_for_cheats(self, start):
        """Check all directions for possible cheats
        This method has the SIDE EFFECT of adding to `cheats`
        when a valid cheat exists"""
        for dp in self.direc_incrs.values():
            self.check_2(start, dp)

    def find_all_cheats(self):
        """Traverse the track, and find all cheats"""
        for point in self.track:
            self.check_point_for_cheats(point)

    def count_cheats_by_savings(self):
        """Return a count how many cheats there are for a given savings"""
        self.find_all_cheats()
        savings = self.cheats.values()
        return Counter(savings)


# def read_data(filename: str):
#     """Read the data into rules and pages"""
#     with open(filename, "r", encoding="utf8") as f:
#         content = f.read()
#     return content


# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    maze = PGrid(filename=filename)
    cheat_counts = maze.count_cheats_by_savings()
    num_ge_100 = sum(val for key, val in cheat_counts.items() if key >= 100)
    return num_ge_100
    # return cheat_counts


# res = part1(FNAME_TEST)
# rich.print(f"""test data: {part1(FNAME_TEST)}""")
rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rich.print(f"""test data: {part2(FNAME_TEST)}""")
rich.print(f"""Problem input: {part2(fname)}""")
