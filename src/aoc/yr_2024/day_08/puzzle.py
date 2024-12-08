#!/usr/bin/env python

"""
1. Use the Puzzle class from day 6 (move to utils?)
  a. Find all point coordinates with a given string.
2. Use the Position class from day 6
  a. Add subtraction operator (vector subtraction) -> increment vector
  b. Add multiplication operator on increment operator to scale and change direction.

3. Find all coordinates of antennas
  a. Use a counter, loop over all lines and chars
  b. Track positions
  c. Frequencies are any of uppercase, lowercase and digits
4. For all pair of antennas of the same frequency, find antinodes.
  a. For a pair
    i. Subtract B - A to get increment.
    ii. Antinodes at B + (B - A) and A + (A - B)
    iii. Track antinodes by frequency
    iv. Antinode positions must be within the map boundaries
5. Count distinct Antinodes

Input is 50x50
test input is 12x12

"""
import logging
from collections import Counter
from itertools import combinations
from pathlib import Path

from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.position import Position

# from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d08.txt"
FNAME_TEST = "test_data.txt"


class PuzzleMap:
    """A puzzle with basic methods"""

    DIRECTIONS = ["^", ">", "v", "<"]
    OBSTACLE = "#"
    INCREMENTS = dict(zip(DIRECTIONS, [(-1, 0), (0, 1), (1, 0), (0, -1)]))

    def __init__(self, filename: str):
        "docstring"
        self.grid = self.read_grid(filename)
        self.min_row = 0
        self.min_col = 0
        self.max_row = len(self.grid) - 1
        self.max_col = len(self.grid[0]) - 1

    def read_grid(self, filename: str) -> list[str]:
        """Read the data into a list of strings"""
        with open(filename, "r", encoding="utf8") as f:
            content = [line.strip() for line in f]
        return content

    def replace_char(self, s: str, n: int, ch: str):
        """Replace the char at string index `n` with ch"""
        if n < 0 or n >= len(s):
            raise ValueError(f"n ({n}) is out of range")
        return s[:n] + ch + s[n + 1 :]

    def draw_grid(
        self,
        filename: str = None,
        labmap: list[str] = None,
    ):
        """Draw map with new obstacles"""
        mylabmap = labmap if labmap else self.grid.copy()
        if filename:
            with open(filename, "w", encoding="utf8") as f:
                for line in mylabmap:
                    f.write(line + "\n")
        else:
            for line in mylabmap:
                rprint(line)
        print()


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


class Puzzle(PuzzleMap):
    """Specifically for day 8"""

    def __init__(self, filename: str, **kwargs):
        "docstring"
        super().__init__(filename, **kwargs)

    def get_coords_with_counter(
        self, grid: list[str] = None, ignores: list[str] = ["."]
    ) -> dict[str, list[tuple[int, int]]]:
        """Map every point into a dict, keyed on char at point. Values are r, c coords"""
        grid = grid if grid else self.grid
        elements = [
            (char, (row, col))
            for row, line in enumerate(grid)
            for col, char in enumerate(line)
        ]
        # Use Counter to group by char
        grouped = Counter()
        # coord is (row, col)
        for char, coord in elements:
            if char not in ignores:  # Skip some characters
                grouped.setdefault(char, []).append(coord)
        return grouped

    def get_n_combinations(self, items: list, n: int = 2) -> list[tuple]:
        """Get a list of all the combinations from items"""
        return list(combinations(items, n))

    def find_antinodes_antenna_pair(self, x: Position, y: Position) -> list[Position]:
        """Find the antinodes of x and y"""
        xx = Position.from_tuple(x) if isinstance(x, tuple) else x
        yy = Position.from_tuple(y) if isinstance(y, tuple) else y
        return xx + (xx - yy), yy + (yy - xx)

    def find_antinodes_antenna_list(self, antennas: list[Position]) -> list[Position]:
        """Find all the antinodes for a list of coordinates"""
        nested_antinodes = [
            self.find_antinodes_antenna_pair(x, y)
            for x, y in self.get_n_combinations(antennas, n=2)
        ]
        antinodes = [pos for items in nested_antinodes for pos in items]
        unique_antinodes = list(set(antinodes))
        sorted_antinodes = Position.sort_positions(unique_antinodes)
        return self.keep_positions_in_grid(sorted_antinodes)

    def keep_positions_in_grid(self, positions: list[Position]) -> list[Position]:
        """Only keep positions that are within the grid"""
        return [pos for pos in positions if self.position_in_grid(pos)]

    def find_all_antinodes(self):
        """Find all the antinodes in the map"""
        coord_dict = self.get_coords_with_counter()
        antinode_dict = {
            key: self.find_antinodes_antenna_list(coords)
            for key, coords in coord_dict.items()
        }
        return antinode_dict

    def position_in_grid(self, pos: Position) -> bool:
        """True if the position is within the grid boundries"""
        return (
            self.min_row <= pos.row <= self.max_row
            and self.min_col <= pos.col <= self.max_col
        )

    def count_distinct_antinodes(self) -> int:
        antinodes_dict = self.find_all_antinodes()
        return len(list(set([x for items in antinodes_dict.values() for x in items])))


# @time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    puzzle = Puzzle(filename)
    puzzle.draw_grid("outmap.txt")
    rprint(puzzle.get_coords_with_counter())
    rprint(puzzle.find_all_antinodes())
    return puzzle.count_distinct_antinodes()


rprint(f"""test data: {part1('test_data_5.txt')}""")
# rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


# @time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


# @time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


rprint(f"""test data: {part2(FNAME_TEST)}""")
# rprint(f"""Problem input: {part2(fname)}""")
