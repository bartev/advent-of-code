#!/usr/bin/env python

import logging
from pathlib import Path

import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.grid_points import Grid
from aoc.pyutils.utils import find_continuous_values, time_it

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
    with open(filename, "r", encoding="utf8") as f:
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
                new_region = self.contiguous_matching_region(point)
                regions.append(new_region)
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

    def find_all_top_points(self, region) -> dict[int, list[int]]:
        """Find all sets of top points
        Result is a dict
        row: list[list[col_indices]]
        """
        cur_region = region.copy()
        res = {}
        while cur_region:
            point_min, _ = self.region_boundaries(cur_region)
            (row, _) = point_min
            # list of ints
            top_col_points = self.find_top_row_points(cur_region)
            top_col_indices = [col for (row, col) in top_col_points]
            # lists of continuous indices
            res[row] = find_continuous_values(top_col_indices, increasing=True)
            points_to_drop_from = [(row, col) for col in top_col_indices]
            cur_region = self.drop_adjacent_points_down(points_to_drop_from, cur_region)
        return res

    def find_all_bottom_points(self, region) -> dict[int, list[int]]:
        """Find all sets of bottom points
        Result is a dict
        row: list[list[col_indices]]
        """
        cur_region = region.copy()
        res = {}
        while cur_region:
            _, point_max = self.region_boundaries(cur_region)
            (row, _) = point_max  # Start from the bottom
            # list of ints
            bottom_col_points = self.find_bottom_row_points(cur_region)
            bottom_col_indices = [col for (row, col) in bottom_col_points]
            # lists of continuous indices
            res[row] = find_continuous_values(bottom_col_indices, increasing=False)
            points_to_drop_from = [(row, col) for col in bottom_col_indices]
            cur_region = self.drop_adjacent_points_up(points_to_drop_from, cur_region)
        return res

    def find_all_left_points(self, region) -> dict[int, list[int]]:
        """Find all sets of left points
        Result is a dict
        row: list[list[col_indices]]
        """
        cur_region = region.copy()
        res = {}
        while cur_region:
            point_min, _ = self.region_boundaries(cur_region)
            (_, col) = point_min
            # list of ints
            left_row_points = self.find_left_col_points(cur_region)
            left_row_indices = [row for (row, col) in left_row_points]
            # lists of continuous indices
            res[col] = find_continuous_values(left_row_indices, increasing=True)
            points_to_drop_from = [(row, col) for row in left_row_indices]
            cur_region = self.drop_adjacent_points_right(
                points_to_drop_from, cur_region
            )
        return res

    def find_all_right_points(self, region) -> dict[int, list[int]]:
        """Find all sets of right points
        Result is a dict
        row: list[list[col_indices]]
        """
        cur_region = region.copy()
        res = {}
        while cur_region:
            _, point_max = self.region_boundaries(cur_region)
            (_, col) = point_max
            # list of ints
            right_row_points = self.find_right_col_points(cur_region)
            right_row_indices = [row for (row, col) in right_row_points]
            # lists of continuous indices
            res[col] = find_continuous_values(right_row_indices, increasing=False)
            points_to_drop_from = [(row, col) for row in right_row_indices]
            cur_region = self.drop_adjacent_points_left(points_to_drop_from, cur_region)
        return res

    def count_nested_lists(self, dlist: dict[list[list]]) -> int:
        """count total number of nested lists in the following structure
        {0: [[0, 1, 2], [4, 5, 6]], 1: [[3], [7, 8]]}
        > 4
        """
        sides_per_row_or_col = [len(nested) for nested in dlist.values()]
        return sum(sides_per_row_or_col)

    def count_sides(self, region: Region):
        tops = self.find_all_top_points(region)
        bottoms = self.find_all_bottom_points(region)
        lefts = self.find_all_left_points(region)
        rights = self.find_all_right_points(region)

        res = {
            "top": {"len": len(tops), "indices": self.count_nested_lists(tops)},
            "bottom": {
                "len": len(bottoms),
                "indices": self.count_nested_lists(bottoms),
            },
            "left": {"len": len(lefts), "indices": self.count_nested_lists(lefts)},
            "right": {"len": len(rights), "indices": self.count_nested_lists(rights)},
        }
        return res

    def fence_price_bulk(self, region) -> int:
        """Return price = Area x Perimeter for region"""
        area = len(region)
        # breakpoint()

        # perimeter = self.perimeter_length(region)
        num_sides = [d["indices"] for d in self.count_sides(region).values()]
        sides = sum(num_sides)
        return area * sides


# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    # part1_test(filename)
    grid = PGrid(filename=filename)
    all_regions = grid.all_contiguous_regions()
    prices = [grid.fence_price(region) for region in all_regions]
    return sum(prices)


rich.print(f"""test data expect 140: {part1(FNAME_TEST)}""")
rich.print(f"""test data 2 expect 772: {part1('test_data_2.txt')}""")
rich.print(f"""test data 2 expect 1930: {part1('test_data_3.txt')}""")
rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    grid = PGrid(filename=filename)
    all_regions = grid.all_contiguous_regions()
    prices = [grid.fence_price_bulk(region) for region in all_regions]
    # for region in all_regions:
    #     rich.print(f"boundaries: {grid.region_boundaries(region)}")
    #     print(grid.count_sides(region))
    #     rich.print(grid.print_positions(region))
    #     rich.print(grid.fence_price_bulk(region))
    #     print()
    return sum(prices)


rich.print(f"""test data: {part2(FNAME_TEST)}""")
rich.print(f"""Problem input: {part2(fname)}""")
