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
            (rr, cc)
            for rr, cc in adj_points
            if self.equals_ref(self.get(rr, cc), ref_val)
        ]
        return valid_points

    def equals_ref(self, value, ref_val) -> bool:
        """Check if a value is valid for comparison."""
        try:
            return int(value) == ref_val
        except ValueError:
            return False

    def adjacent_p1_points_list(
        self, positions: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Apply adjacent_p1_points on a list of positions"""
        if len(positions) > 0:
            with_dupes = [self.adjacent_p1_points(row, col) for (row, col) in positions]
            flattened = [item for sublist in with_dupes for item in sublist]
            no_dupes = list(set(flattened))
        else:
            no_dupes = []
        return no_dupes

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

    def count_peaks_from_head(self, row: int, col: int) -> int:
        """Count the number of peaks you can reach from row, col"""
        # 1's is a special case. There's only 1 starting point
        ones = self.adjacent_p1_points(row, col)
        # 2's - 9's can start with a list
        twos = self.adjacent_p1_points_list(ones)
        threes = self.adjacent_p1_points_list(twos)
        fours = self.adjacent_p1_points_list(threes)
        fives = self.adjacent_p1_points_list(fours)
        sixes = self.adjacent_p1_points_list(fives)
        sevens = self.adjacent_p1_points_list(sixes)
        eights = self.adjacent_p1_points_list(sevens)
        peaks = self.adjacent_p1_points_list(eights)
        return len(peaks)


def flatten(nested: list[list]) -> list:
    """Flatten a list of lists"""
    return [item for sublist in nested for item in sublist]


def remove_duplicates(xs: list) -> list:
    return list(set(xs))


def fooling_around(grid: Grid) -> None:
    # rprint(grid)
    # md = grid.all_m_distances(1, 2)
    # rprint()
    # md.print_grid()
    # rprint()
    rprint(f"{grid.positions_within_dist(row_start=1, col_start=2, distance=1)=}")
    rprint(f"(1, 2): {grid.adjacent_p1_points(1, 2)=}")
    # rprint(f"(2, 1): {grid.adjacent_p1_points(2, 1)=}")
    # rprint("adjacent p1 positions to 2, 1")
    # rprint(grid.print_positions(grid.adjacent_p1_points(2, 1)))
    #
    # trail_heads = grid.find_trail_heads()
    # rprint(f"{trail_heads=}")
    # print()
    # rprint(grid.print_positions(trail_heads))
    #
    rprint(f"{grid.positions_within_dist(0, 0,distance=2)=}")
    # rprint(f"{grid.find_nearby_values(row=0, col=0, distance=2, search_val=8)=}")
    # rprint(f"{grid.find_nearby_values(0, 0, 2, 1)=}")
    # rprint(f"{grid.find_nearby_values(0, 0, 3, 2)=}" "")
    # ----
    # rprint(Rule("good above here", style="bold red"))

    # rprint(f"{grid.positions_within_dist(0, 0, 5)=}")

    # rprint("grid.count_nearby_peaks(0, 0, 4)=")
    # rprint(grid.count_nearby_peaks(0, 0, 4))

    rprint(f"{grid.count_peaks_from_head(0, 0)=}")


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    grid = PGrid(filename=filename)

    # TEST_FUN = True
    TEST_FUN = False
    if TEST_FUN:
        fooling_around(grid)
    else:
        # rprint(Rule("Part 1 start solving", style="bold red"))
        trail_heads = grid.find_trail_heads()
        # rprint(f"{trail_heads=}")
        nearby_positions = {
            (row, col): grid.positions_within_dist(row, col, 9)
            for (row, col) in trail_heads
        }
        peak_counts = {
            (row, col): grid.count_peaks_from_head(row, col)
            for (row, col) in trail_heads
        }
        # rprint(f"{peak_counts=}")
        return sum(peak_counts.values())


rprint(f"""test data (expect 1): {part1(FNAME_TEST)}""")
rprint(f"""test data (expect 2): {part1('test_data_score_2.txt')=}""")
rprint(f"""test data (expect 4): {part1('test_data_score_4.txt')=}""")
rprint(f"""test data (expect 2, 1): {part1('test_data_score_2b.txt')=}""")
rprint(f"""test data (expect 36): {part1('test_data_score_36.txt')=}""")

rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
