#!/usr/bin/env python

import logging
from pathlib import Path

from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.grid_points import Grid
from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d12.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = f.read()
    return content


Point = tuple[int, int]  # (row, col)
Region = list[Point]


class PGrid(Grid):
    """Grid for this puzzle"""

    def adjacent_matching_points(self, point: Point) -> Region:
        """Return all adjacent points that have the same value"""
        adj_points = self.positions_within_dist(point, distance=1)
        ref_val = self.get(point)
        valid_points = [pt for pt in adj_points if self.get(pt) == ref_val]
        return valid_points

    def contiguous_matching_region(self, point: Point) -> Region:
        """Find all points contiguous to point with the same value"""
        pt_value = self.get(point)
        search_region = {point}
        acc_region = set()
        pt = search_region.pop()
        while pt:
            if pt not in acc_region:
                acc_region.add(pt)
            [
                search_region.add(new_pt)
                for new_pt in self.adjacent_matching_points(pt)
                if new_pt not in acc_region and new_pt not in search_region
            ]
            pt = search_region.pop() if search_region else None
        return acc_region

    def all_contiguous_regions(self) -> list[Region]:
        """Find all contiguos regions defined as having
        up/down/left/right neighbors with the same value
        """
        points_seen = set()
        regions = []
        # Iterate over all points in the grid until all points have
        # been seen.
        for row in range(self.rows):
            for col in range(self.cols):
                point = (row, col)
                if point in points_seen:
                    continue
                else:
                    new_region = self.contiguous_matching_region(point)
                    regions.append(new_region)
                    # breakpoint()

                    points_seen = points_seen.union(new_region)
        return regions

    def get_region_value(self, region: Region):
        """Get the value of the cells in `region`"""
        return self.get(next(iter(region)))

    def perimeter_length(self, region: Region) -> int:
        """The length of the perimeter for each point in the region,
        the perimeter is 4 - the number of neighbors.
        """
        num_neighbors = [len(self.adjacent_matching_points(point)) for point in region]
        num_cells = len(region)
        return 4 * num_cells - sum(num_neighbors)

    def fence_price(self, region) -> int:
        """Return price = Area x Perimeter for region"""
        area = len(region)
        perimeter = self.perimeter_length(region)
        return area * perimeter


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


def grid_point_tests():
    """"""

    "Check some methods as I modify them" ""
    grid = PGrid(filename=FNAME_TEST)
    assert grid.in_grid((2, 2))
    assert not grid.in_grid((2, 7))
    assert grid.get((1, 3)) == "D"


grid_point_tests()


def part1_test(filename: str) -> int:
    """Testing stuff for part 1"""
    grid = PGrid(filename=filename)
    grid.print_grid()
    match_region_00 = grid.contiguous_matching_region((0, 0))
    print(f"{match_region_00=}")
    all_regions = grid.all_contiguous_regions()
    print(f"{all_regions=}")
    for region in all_regions:
        region_val = grid.get_region_value(region)
        perimeter = grid.perimeter_length(region)
        price = grid.fence_price(region)
        print(f"{region_val=}, {perimeter=}, {price=}")
        rprint(grid.print_positions(region))


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    # part1_test(filename)
    grid = PGrid(filename=filename)
    all_regions = grid.all_contiguous_regions()
    prices = [grid.fence_price(region) for region in all_regions]
    return sum(prices)


rprint(f"""test data expect 140: {part1(FNAME_TEST)}""")
rprint(f"""test data 2 expect 772: {part1('test_data_2.txt')}""")
rprint(f"""test data 2 expect 1930: {part1('test_data_3.txt')}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


rprint(f"""test data: {part2(FNAME_TEST)}""")
# rprint(f"""Problem input: {part2(fname)}""")
