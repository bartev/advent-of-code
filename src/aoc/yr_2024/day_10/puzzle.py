#!/usr/bin/env python

"""
For each trailhead (0), how many peaks (9's) can
I get to by increasing by only 1, and
moving up/down/left/right?

1. How many trailheads in the map?
   a. Number 0-num_heads with coordinates
2. How many peaks total?
   a. Number 0-num_peaks with coordinates
3. How many peaks within 9 steps? (manhattan distance)
4. For a given position, where can I move
   a. At most 4 for a trailhead
   b. At most 3 for everywhere else


Stopping conditions
1. I've reached all the peaks
2. All my trails have hit a peak or dead end


"""
import logging
from pathlib import Path

from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.grid import Grid
from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d10.txt"
FNAME_TEST = "test_data.txt"


# def read_data(filename: str):
#  """Read the data into rules and pages"""
#     with open(filename, "r") as f:
#         content = f.read()
#     return content


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


class PGrid(Grid):
    """Grid for this Puzzle"""

    def find_trail_heads(self):
        """Find all trailheads (val = 0)"""
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.get(row, col) == "0"
        ]

    def print_positions(self, positions: list[tuple]):
        """Print the grid with only the positions shown"""
        pos_grid = PGrid(rows=self.rows, cols=self.cols)
        for row, col in positions:
            val = self.get(row, col)
            pos_grid.set(row, col, val)
        return pos_grid

    def adjacent_p1_points(self, row, col) -> list[tuple[int, int]]:
        """Return all adjacent points that are increasing in value by 1"""
        adj_points = self.positions_within_dist(row, col, distance=1)
        ref_val = int(self.get(row, col)) + 1
        valid_points = [
            (rr, cc) for rr, cc in adj_points if int(self.get(rr, cc)) == ref_val
        ]
        return valid_points

    def find_nearby_values(
        self, row, col, distance: int, search_val: int | str
    ) -> list[tuple[int, int]]:
        """Get a list of peaks (9) within distance"""
        value = str(search_val)
        possible_points = self.positions_within_dist(row, col, distance)
        return [(rr, cc) for (rr, cc) in possible_points if self.get(rr, cc) == value]

    def count_nearby_peaks(self, row, col, distance) -> int:
        """Count how many peaks are within distance"""
        nearby = self.find_nearby_values(row, col, distance, 9)
        return len(nearby)


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    grid = PGrid(filename=filename)
    rprint(grid)
    md = grid.all_m_distances(1, 2)
    rprint()
    md.print_grid()
    rprint()
    within_3 = grid.positions_within_dist(1, 2, 1)
    rprint(f"{within_3}")
    next_points = grid.adjacent_p1_points(1, 2)
    rprint(f"{next_points=}")
    next_points = grid.adjacent_p1_points(2, 1)
    rprint(f"{next_points=}")
    rprint(grid.print_positions(next_points))
    trail_heads = grid.find_trail_heads()
    rprint(f"{trail_heads}")
    rprint(grid.print_positions(trail_heads))
    rprint(grid.find_nearby_values(0, 0, 2, 8))
    rprint(grid.find_nearby_values(0, 0, 2, 1))
    rprint(grid.find_nearby_values(0, 0, 3, 2))
    rprint(f"{grid.count_nearby_peaks(0, 0, 4)=}")


rprint(f"""test data: {part1(FNAME_TEST)}""")
# rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
