#!/usr/bin/env python

import logging
import math
import re
from collections import Counter
from pathlib import Path

import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.grid_points import Grid

# from aoc.pyutils.grid_points import Grid
from aoc.pyutils.position import Position
from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d14.txt"
FNAME_TEST = "test_data.txt"

Point = tuple[int, int]  # (row, col)
Region = list[Point]


class Robot(Position):
    """Position of robot with teleport move"""

    def __init__(self, row: int, col: int, vrow: int, vcol: int):
        "Initialize a robot"
        super().__init__(row=row, col=col)
        self.vrow = vrow
        self.vcol = vcol

    def move(
        self,
        grid: Grid,
        steps: int = 1,
    ):
        """Move by vel each step (with teleport)"""
        new_row = self.row + steps * self.vrow
        new_col = self.col + steps * self.vcol
        nrows = grid.rows
        ncols = grid.cols
        self.row = new_row % nrows
        self.col = new_col % ncols

    @property
    def position(self) -> Position:
        return Position(self.row, self.col)

    @property
    def velocity(self) -> Position:
        return Position(self.vrow, self.vcol)

    def __repr__(self):
        """Provide a string representation of the position."""
        return f"Pos(row={self.row}, col={self.col}), Vel(row={self.vrow}, col={self.vcol})"


class PGrid(Grid):
    """Grid for this puzzle with teleport moves"""

    def draw_robots(self, robots: list[Robot]):
        """Draw a grid with a number indicating how many robots are on each position
        (last digit only)
        """
        # list of tuples (row, col)
        robot_positions = [robot.pos for robot in robots]
        res = self.print_on_grid(robot_positions)
        rich.print(res)
        robot_counts = Counter(robot_positions)
        rich.print(robot_counts)

    def robot_position_counts(self, region: Region):
        """Given a list of robot positions, count how many are in each space"""
        return Counter(region)

    def draw_counts_on_grid(self, region: Region):
        """Print count of robots for every point in region"""
        pos_grid = Grid(rows=self.rows, cols=self.cols)
        robot_pos_counts = self.robot_position_counts(region)

        for point, cnt in robot_pos_counts.items():
            char = str(cnt)[-1]
            pos_grid.set(point, char)
        print("print me")
        rich.print(pos_grid)
        return pos_grid

    def count_per_quadrant(self, region: Region):
        """Count how many robots per quadrant"""
        mid_row = (self.rows - 1) // 2
        mid_col = (self.cols - 1) // 2
        robot_pos_counts = self.robot_position_counts(region)
        q1 = 0
        q2 = 0
        q3 = 0
        q4 = 0
        for point, cnt in robot_pos_counts.items():
            row, col = point
            if row < mid_row and col < mid_col:
                q1 += cnt
            elif row < mid_row and col > mid_col:
                q2 += cnt
            elif row > mid_row and col > mid_col:
                q3 += cnt
            elif row > mid_row and col < mid_col:
                q4 += cnt
        # print(f"{mid_row=}, {mid_col=}")
        # rich.print(f"{robot_pos_counts=}")
        return q1, q2, q3, q4


def parse_line(line: str):
    """Parse position and vel from line
    p = x, y, v = dx, dy
    Example
    p=0,4 v=3,-3
    """
    # regex to extract number (with optional negative)
    pat = r"-?\d+"
    numbers = re.findall(pat, line.strip())
    as_ints = list(map(int, numbers))
    x, y, dx, dy = as_ints
    return Robot(row=y, col=x, vrow=dy, vcol=dx)
    # return ((y, x), (dy, dx))


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        lines = [parse_line(line) for line in f if line]
    return lines


def get_robot_positions(region: Region):
    """Get the positions (as tuples) of each robot"""
    return [robot.pos for robot in region]


def safety_factor(robots: Region, grid: PGrid):
    """The safety factor is the product of the counts per quadrant"""
    cnt_per_quad = grid.count_per_quadrant(get_robot_positions(robots))
    return math.prod(cnt_per_quad)


# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


def move_n(grid: PGrid, robots: list[Robot], steps: int = 1):
    """return the robots after moving them n times"""
    [robot.move(grid, steps=steps) for robot in robots]
    return robots


@time_it
def part1(filename: str, rows: int, cols: int) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    robots = read_data(filename)
    # rich.print(robots)
    grid = PGrid(rows=rows, cols=cols)
    robot_positions = get_robot_positions(robots)

    print()
    grid.draw_counts_on_grid(get_robot_positions(robots))
    # [robot.move(grid, steps=100) for robot in robots]
    robots = move_n(grid, robots, steps=100)
    # print("After 100 moves")
    # grid.draw_counts_on_grid(get_robot_positions(robots))
    cnt_per_quad = grid.count_per_quadrant(get_robot_positions(robots))  #
    return safety_factor(robots=robots, grid=grid)


rich.print(f"""test data: {part1(FNAME_TEST, rows=7, cols=11)}""")
rich.print(f"""Problem input: {part1(fname, rows=103, cols=101)}""")

# ########## Part 2

# rich.print(Rule("Part 2", style="bold red"))
# rich.print_json(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rprint(f"""test data: {part2(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part2(fname)}""")
